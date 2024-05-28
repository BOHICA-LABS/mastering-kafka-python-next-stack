import faust

app = faust.App('myapp_consumer', broker='kafka://localhost:9092', web_port=6068)


class Message(faust.Record):
    text: str


topic = app.topic('my-topic', value_type=Message)


@app.agent(topic)
async def process(messages):
    async for message in messages:
        print(f'Received message: {message.text}')


if __name__ == '__main__':
    app.main()
