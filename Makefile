
.PHONY: build run

build: 
	@docker build -t email_notifier .

run:
	@docker run --rm \
	-v ${PWD}:/app \
	--env-file .env \
	email_notifier
