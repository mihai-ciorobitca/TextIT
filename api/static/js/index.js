document.addEventListener('DOMContentLoaded', () => {
  const messageContainer = document.getElementById("message-container");
  const messageForm = document.getElementById("message-form");
  const messageInput = document.getElementById("message-input");

  const initSupabase = () => {
    const supabaseUrl = 'https://dehbokxgefzkgmjlpxme.supabase.co';
    const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlaGJva3hnZWZ6a2dtamxweG1lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY2MjE4MzgsImV4cCI6MjAzMjE5NzgzOH0.1mRW2FizO4Fg4kZY0942lBRJj5I9X4UO6ThKjS6kAQI';
    return supabase.createClient(supabaseUrl, supabaseKey);
  }

  const loadSupabase = () => {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js';
    script.onload = () => {
      const supabase = initSupabase();

      // Fetch initial messages
      fetchMessages(supabase);

      // Subscribe to Supabase Realtime changes
      const channel = supabase
        .channel('public:messages')
        .on('postgres_changes', { event: '*', schema: 'public', table: 'messages' }, payload => {
          renderMessage(payload.new);
        })
        .subscribe();
    };
    script.onerror = (error) => {
      console.error('Error loading Supabase:', error);
    };
    document.head.appendChild(script);
  };

  loadSupabase();

  // Handle message submission
  messageForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = messageInput.value;

    const maxRetries = 3; // Maximum number of retries
    let retries = 0; // Current number of retries

    const sendMessage = async () => {
      try {
        await fetch('/send_message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text })
        });
        messageInput.value = '';
      } catch (error) {
        if (error.name === 'ConnectTimeout' && retries < maxRetries) {
          retries++;
          console.log(`Retrying send message (${retries}/${maxRetries})`);
          setTimeout(sendMessage, 2000); // Retry after 2 seconds
        } else {
          console.error('Error sending message:', error);
        }
      }
    };

    sendMessage();
  });

  // Fetch and render initial messages
  async function fetchMessages(supabase) {
    const { data, error } = await supabase
      .from('messages')
      .select('*');

    if (error) {
      console.error('Error fetching messages:', error);
    } else {
      data.forEach(message => {
        renderMessage(message);
      });
    }
  }

  // Render a message in the message container
  function renderMessage(message) {
    const messageItem = document.createElement("div");
    messageItem.classList.add("bg-light", "rounded", "p-2", "mb-2");
    messageItem.style.maxWidth = "75%";
    messageItem.textContent = message.text;
    if (message.sender === "{{ email }}") {
      messageItem.classList.add("align-self-end");
    } else {
      messageItem.classList.add("align-self-start");
    }
    messageContainer.prepend(messageItem);
    messageContainer.scrollTop = messageContainer.scrollHeight;
  }
});
