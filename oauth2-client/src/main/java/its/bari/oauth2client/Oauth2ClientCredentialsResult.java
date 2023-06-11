package its.bari.oauth2client;

record Oauth2ClientCredentialsResult(
        String access_token,
        long expires_in,
        long refresh_expires_in,
        String token_type,
        String scope
) {
    public boolean isCorrect() {
        return access_token != null && !access_token.isBlank();
    }
}
