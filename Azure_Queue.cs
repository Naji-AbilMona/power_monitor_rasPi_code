using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Azure.ServiceBus;

namespace main1
{
    class Program
    {
        const string ServiceBusConnectionString = "Endpoint=sb://powermonitor.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=1ANZ4ZRIKIIW4EBc8a6P586klbcB0x+wXrrcaZs6+B0=";
        const string QueueName = "mr.q";
        static IQueueClient queueClient;
        public static async Task Main(string[] args)
        {
            const int numberOfMessages = 2;
            queueClient = new QueueClient(ServiceBusConnectionString, QueueName);

            Console.WriteLine("======================================================");
            Console.WriteLine("Press ENTER key to exit after sending all the messages.");
            Console.WriteLine("======================================================");

            // Send messages.
            await SendMessagesAsync(numberOfMessages);

            Console.ReadKey();

            await queueClient.CloseAsync();
        }
        static async Task SendMessagesAsync(int numberOfMessagesToSend)
        {
            try
            {
                for (var i = 0; i < numberOfMessagesToSend; i++)
                {
                    // Create a new message to send to the queue.
                    string messageBody = $"123";
                    var message = new Message(Encoding.UTF8.GetBytes(messageBody));
                   // var message = new Message(123);

                    // Write the body of the message to the console.
                    Console.WriteLine($"Sending message: {message}");

                    // Send the message to the queue.
                    await queueClient.SendAsync(message);
                }
            }
            catch (Exception exception)
            {
                Console.WriteLine($"{DateTime.Now} :: Exception: {exception.Message}");
            }
        }
    }
}
