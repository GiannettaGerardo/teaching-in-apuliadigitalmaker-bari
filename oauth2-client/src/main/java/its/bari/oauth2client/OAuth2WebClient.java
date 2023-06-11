package its.bari.oauth2client;

import org.springframework.web.reactive.function.client.WebClient;

/**
 * Interface to be implemented to create authorized http requests.
 */
public interface OAuth2WebClient {
    /**
     * Make an authorized http request.
     * @param preparedWebClient http request to execute already set.
     * @param classToUse class of the object returned by the http request.
     * @return the result of the http request.
     * @throws Exception if an unrecoverable error occurs.
     */
    Object authorizedHttpRequest(WebClient.RequestHeadersSpec<?> preparedWebClient, Class<?> classToUse) throws Exception;

    /**
     * Make an authorized http request.
     * @param preparedWebClient http request to execute already set.
     * @param classToUse class of the object returned by the http request.
     * @param millis array of milliseconds representing the http request
     *               retry logic in case of failure.
     * @return the result of the http request.
     * @throws Exception if an unrecoverable error occurs.
     */
    Object authorizedHttpRequest(WebClient.RequestHeadersSpec<?> preparedWebClient, Class<?> classToUse, int[] millis) throws Exception;
}
