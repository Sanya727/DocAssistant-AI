document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('queryForm');

  form.addEventListener('submit', async (event) => {
      event.preventDefault(); // Prevent the default form submission

      const query = document.getElementById('aiQuery').value; // Get the input value

      try {
          const response = await fetch('/ai', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ query })
          });

          const result = await response.json();
          const resultElement = document.getElementById('queryResult');
          resultElement.innerText = result.Answer;
      } catch (error) {
          console.error('Error:', error);
      }
  });
});
