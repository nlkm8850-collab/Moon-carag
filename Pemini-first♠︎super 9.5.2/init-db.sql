-- Pemini Girl 9.5.2 - Database Initialization
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_snippets_user_id ON code_snippets(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(token);
