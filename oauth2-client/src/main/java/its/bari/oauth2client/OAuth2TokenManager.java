package its.bari.oauth2client;


import java.time.Instant;

class OAuth2TokenManager {
    private final Oauth2ClientCredentialsResult token;
    private final long tokenCreationEpoch;

    OAuth2TokenManager(final Oauth2ClientCredentialsResult token) {
        this.tokenCreationEpoch = Instant.now().getEpochSecond();
        this.token = token;
    }

    public boolean tokenIsReusable() {
        return ((tokenCreationEpoch + token.expires_in()) - Instant.now().getEpochSecond()) > 60;
    }

    public Oauth2ClientCredentialsResult getToken() {
        return token;
    }

    public long getTokenCreationEpoch() {
        return tokenCreationEpoch;
    }
}
