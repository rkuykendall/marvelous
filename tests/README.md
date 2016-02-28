# Testing

These tests use the marvelous requests caching for mocking tests, so tests will
run quickly and not require an API key on travis, which may fail due to
rate limiting.

If your code adds a new URL to the cache, set the `PUBLIC_KEY` and
`PRIVATE_KEY` environment variables before running the test and it will be
populated in the `testing_mock.sqlite` database.

At any point you should be able to delete the database, set any API keys, and
run the full test suite to repopulate it.
