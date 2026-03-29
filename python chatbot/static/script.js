let currentQuestionIndex = 0;
let totalQuestions = 0;
let selectedOption = null;
let quizActive = false;
let answerChecked = false;

function startQuiz() {
    const level = document.getElementById('levelSelect').value;
    const numQuestions = document.getElementById('questionCount').value;
    
    fetch('/start_quiz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            level: level,
            num_questions: parseInt(numQuestions)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Hide setup, show chat
        document.getElementById('quizSetup').style.display = 'none';
        document.getElementById('chatContainer').style.display = 'block';
        
        // Store quiz info
        currentQuestionIndex = 1;
        totalQuestions = data.total_questions;
        quizActive = true;
        answerChecked = false;
        
        // Display first question
        displayQuestion(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to start quiz. Please try again.');
    });
}

function displayQuestion(data) {
    const chatMessages = document.getElementById('chatMessages');
    const optionsContainer = document.getElementById('optionsContainer');
    const explanationBox = document.getElementById('explanationBox');
    const nextBtn = document.getElementById('nextBtn');
    
    // Hide explanation and next button for new question
    explanationBox.style.display = 'none';
    nextBtn.style.display = 'none';
    
    // Add bot message with question
    const questionHtml = `
        <div class="message">
            <div class="bot-message">
                <strong>Question ${data.question_number}/${data.total_questions}:</strong><br>
                ${data.question}
            </div>
        </div>
    `;
    chatMessages.innerHTML += questionHtml;
    
    // Add options
    let optionsHtml = '';
    data.options.forEach((option, index) => {
        optionsHtml += `<button class="option-btn" onclick="selectOption(${index})">${option}</button>`;
    });
    optionsContainer.innerHTML = optionsHtml;
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function selectOption(index) {
    if (answerChecked) return; // Prevent selecting after answer checked
    
    // Remove selected class from all options
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Add selected class to clicked option
    document.querySelectorAll('.option-btn')[index].classList.add('selected');
    selectedOption = index;
}

function checkAnswer() {
    if (selectedOption === null) {
        alert('Please select an answer!');
        return;
    }
    
    // Disable all options
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.disabled = true;
    });
    
    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            selected_option: selectedOption
        })
    })
    .then(response => response.json())
    .then(data => {
        answerChecked = true;
        
        // Add user's answer to chat
        const chatMessages = document.getElementById('chatMessages');
        const selectedOptionText = document.querySelectorAll('.option-btn')[selectedOption].textContent;
        
        const userAnswerHtml = `
            <div class="message">
                <div class="user-message">${selectedOptionText}</div>
            </div>
        `;
        chatMessages.innerHTML += userAnswerHtml;
        
        // Show explanation
        const explanationBox = document.getElementById('explanationBox');
        const correctStatus = data.is_correct ? '✅ Correct!' : '❌ Incorrect!';
        explanationBox.innerHTML = `
            <strong>${correctStatus}</strong><br>
            Correct answer: ${data.correct_answer}<br>
            <em>${data.explanation}</em><br>
            Current score: ${data.score}
        `;
        explanationBox.style.display = 'block';
        
        // Show next button
        document.getElementById('nextBtn').style.display = 'inline-block';
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to check answer. Please try again.');
    });
}

function nextQuestion() {
    if (!answerChecked) {
        checkAnswer();
        return;
    }
    
    fetch('/next_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.quiz_complete) {
            // Quiz completed
            showFinalScore(data);
        } else {
            // Reset for next question
            selectedOption = null;
            answerChecked = false;
            
            // Hide explanation and next button
            document.getElementById('explanationBox').style.display = 'none';
            document.getElementById('nextBtn').style.display = 'none';
            
            // Display next question
            displayQuestion(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to load next question. Please try again.');
    });
}

function showFinalScore(data) {
    const chatMessages = document.getElementById('chatMessages');
    const optionsContainer = document.getElementById('optionsContainer');
    const explanationBox = document.getElementById('explanationBox');
    const nextBtn = document.getElementById('nextBtn');
    const restartBtn = document.getElementById('restartBtn');
    
    // Clear options
    optionsContainer.innerHTML = '';
    
    // Hide explanation and next button
    explanationBox.style.display = 'none';
    nextBtn.style.display = 'none';
    
    // Show final score
    const scoreHtml = `
        <div class="message">
            <div class="bot-message">
                <div class="score-box">
                    <h3>🎉 Quiz Completed! 🎉</h3>
                    <p>Your final score: ${data.final_score}/${data.total_questions}</p>
                    <div class="percentage">${data.percentage.toFixed(1)}%</div>
                </div>
            </div>
        </div>
    `;
    chatMessages.innerHTML += scoreHtml;
    
    // Show restart button
    restartBtn.style.display = 'inline-block';
    
    quizActive = false;
}

function restartQuiz() {
    fetch('/restart_quiz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        // Reset UI
        document.getElementById('quizSetup').style.display = 'block';
        document.getElementById('chatContainer').style.display = 'none';
        document.getElementById('chatMessages').innerHTML = '';
        document.getElementById('optionsContainer').innerHTML = '';
        document.getElementById('explanationBox').style.display = 'none';
        document.getElementById('nextBtn').style.display = 'none';
        document.getElementById('restartBtn').style.display = 'none';
        
        // Reset variables
        currentQuestionIndex = 0;
        totalQuestions = 0;
        selectedOption = null;
        quizActive = false;
        answerChecked = false;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to restart quiz. Please refresh the page.');
    });
}

// Add event listener for option clicks that automatically checks answer
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('option-btn') && !answerChecked && quizActive) {
        // Small delay to ensure the selected class is added
        setTimeout(() => {
            if (selectedOption !== null) {
                checkAnswer();
            }
        }, 100);
    }
});