-- chatbot.chat_logs definition

-- Drop table

-- DROP TABLE chatbot.chat_logs;

CREATE TABLE chatbot.chat_logs (
	id uuid NOT NULL,
	user_message text NOT NULL,
	ai_response text NOT NULL,
	model_used varchar(50) NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	user_name text NULL,
	CONSTRAINT chat_logs_pkey PRIMARY KEY (id)
);