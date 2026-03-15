-- Optional seed data

INSERT INTO users (id, name) VALUES
  (1, 'Alice'),
  (2, 'Bob')
ON DUPLICATE KEY UPDATE name = VALUES(name);
