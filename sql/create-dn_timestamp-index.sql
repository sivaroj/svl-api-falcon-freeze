CREATE INDEX idx_dn_timestamp_MD5 ON dn_timestamp USING BTREE ((data->>'MD5'));
CREATE INDEX idx_dn_timestamp_DN_NO ON dn_timestamp USING BTREE ((data->>'DN_NO'));