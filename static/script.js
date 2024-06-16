function askGPT() {
  var userInput = document.getElementById('userInput').value;
   if (userInput.trim() === '') return; // Don't send empty messages
  addMessageToConversation('user-message', userInput);
  fetch('/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'user_input=' + encodeURIComponent(userInput)
  })
  .then(response => response.json())
  .then(data => {
    // Правильно обращаемся к свойству 'message' объекта ответа
    addMessageToConversation('gpt-message', data.message);
  })
  .catch(error => console.error('Error:', error));
  // Clear the input field
  document.getElementById('userInput').value = '';
}

function addMessageToConversation(className, message) {
  const conversationElement = document.getElementById('conversation');
  const messageElement = document.createElement('li');
  const messageContent = document.createElement('span');
  const messageIcon = document.createElement('span');

  messageElement.className = className;
  messageContent.className = 'message-content';
  messageContent.textContent = message;
  messageIcon.className = 'message-icon';

  // Выберите иконку или emoji для пользователя и нейросети
  if (className === 'user-message') {
    messageIcon.textContent = '👤'; // Или '<i class="fas fa-user"></i>' для Font Awesome
    messageElement.appendChild(messageContent);
    messageElement.appendChild(messageIcon);
  } else {
    messageIcon.textContent = '🤖'; // Или '<i class="fas fa-robot"></i>' для Font Awesome
    messageElement.appendChild(messageIcon);
    messageElement.appendChild(messageContent);
  }

  conversationElement.appendChild(messageElement);

  // Прокрутка к последнему сообщению
  conversationElement.scrollTop = conversationElement.scrollHeight;
}


function handleKeyPress(event) {
  // If the user presses the "Enter" key, call askGPT()
  if (event.key === 'Enter') {
    askGPT();
  }
}