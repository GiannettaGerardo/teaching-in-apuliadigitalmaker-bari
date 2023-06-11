package its.bari.oauth2client;

import its.bari.oauth2client.exception.OAuth2ClientIs4xxException;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

import java.time.Duration;

public class OAuth2WebClientImpl implements OAuth2WebClient {
    private final String clientId;
    private final String clientSecret;
    private final String tokenUri;
    private final WebClient webClient;
    private OAuth2TokenManager tokenManager;

    /**
     * Requests the first access token from the authorization server.
     * @param clientId oauth2 client id.
     * @param clientSecret oauth2 client secret.
     * @param tokenUri oauth2 uri to request a token.
     * @param webClient the webclient that will execute the token requests.
     * @throws Exception if an unrecoverable error occurs.
     */
    public OAuth2WebClientImpl(String clientId, String clientSecret, String tokenUri, WebClient webClient) throws Exception {
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.tokenUri = tokenUri;
        this.webClient = webClient;
        this.getAccessToken();
    }

    /**
     * It is the only secure access point to the oauth2 access token obtained from the authorization
     * server, because the method is synchronized. Requests a new access token only if the currently
     * saved token is marked as 'reusable' by the tokenManager.
     * @throws Exception if an unrecoverable error occurs.
     * @synchronized
     */
    private synchronized Oauth2ClientCredentialsResult getValidToken() throws Exception {
        if (tokenManager.tokenIsReusable()) {
            System.err.println("getValidToken -> uso : " + tokenManager.getToken().access_token());
            return tokenManager.getToken();
        }
        System.err.println("getValidToken -> nuova richiesta");
        this.getAccessToken();
        System.err.println("getValidToken -> nuovo token : " + tokenManager.getToken().access_token());
        return tokenManager.getToken();
    }

    /**
     * Request a new access token from the authorization server. Implements a 3-times backoff + jitter
     * failure retry policy. The resulting token is placed inside the tokenManager.
     * @throws Exception if an unrecoverable error occurs.
     */
    private void getAccessToken() throws Exception {
        Oauth2ClientCredentialsResult result = null;
        try {
            result = webClient
                    .post()
                    .uri(tokenUri)
                    .header(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE)
                    .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                    .body(BodyInserters
                            .fromFormData("grant_type", "client_credentials")
                            .with("client_id", clientId)
                            .with("client_secret", clientSecret)
                    )
                    .retrieve()
                    .onStatus(HttpStatusCode::isError, clientResponse -> Mono.error(new Exception("onStatus error...")))
                    .bodyToMono(Oauth2ClientCredentialsResult.class)
                    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1)).jitter(0.75)
                            .onRetryExhaustedThrow((retryBackoffSpec, retrySignal) -> {
                                throw new RuntimeException("getAccessToken -> onRetryExhaustedThrow");
                            })
                    ).block();
        } catch (Exception e) {
            throw new Exception("catch exception...");
        }
        if (result == null || !result.isCorrect()) {
            throw new Exception("result null or not correct...");
        }
        this.tokenManager = new OAuth2TokenManager(result);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public Object authorizedHttpRequest(
            final WebClient.RequestHeadersSpec<?> preparedWebClient,
            final Class<?> classToUse
    ) throws Exception {
        return this.authorizedHttpRequest(preparedWebClient, classToUse, new int[]{});
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public Object authorizedHttpRequest(
            final WebClient.RequestHeadersSpec<?> preparedWebClient,
            final Class<?> classToUse,
            final int[] millis
    ) throws Exception {
        int i = 0;
        while (true) {
            final Oauth2ClientCredentialsResult completeToken = this.getValidToken();
            try {
                return preparedWebClient
                        .header(HttpHeaders.AUTHORIZATION, "Bearer " + completeToken.access_token())
                        .retrieve()
                        .onStatus(HttpStatusCode::is4xxClientError, response -> Mono.error(new OAuth2ClientIs4xxException()))
                        .onStatus(HttpStatusCode::is5xxServerError, response -> Mono.error(new Exception()))
                        .bodyToMono(classToUse)
                        .block();
            } catch (OAuth2ClientIs4xxException e) {
                if (i >= millis.length) {
                    throw new OAuth2ClientIs4xxException();
                }
                Thread.sleep(millis[i]);
                i++;
            } catch (Exception e) {
                throw new Exception("Errore");
            }
        }
    }

}
