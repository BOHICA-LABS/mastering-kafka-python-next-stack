import faust
import time

app = faust.App('myapp_producer', broker='kafka://localhost:9092', web_port=6067)


class Message(faust.Record):
    text: str


topic = app.topic('my-topic', value_type=Message)


@app.timer(interval=1.0)
async def produce():
    for i in range(10):
        message = Message(text=f'Message {i}')
        await topic.send(value=message)
        print(f'Sent message: {message.text}')
        time.sleep(1)


if __name__ == '__main__':
    app.main()
