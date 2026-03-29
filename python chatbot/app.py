from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from quiz_data import quiz_questions, get_questions_by_level
import random

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credentials
app.secret_key = 'your_secret_key_here_change_this_in_production'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Fix for cookie issues

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    """Initialize a new quiz session"""
    try:
        data = request.json
        level = data.get('level', 'beginner')
        num_questions = data.get('num_questions', 5)
        
        # Get questions for the selected level
        questions = get_questions_by_level(level, num_questions)
        
        if not questions:
            return jsonify({'error': 'No questions available for this level'}), 400
        
        # Store quiz data in session
        session['quiz'] = {
            'questions': questions,
            'current_index': 0,
            'score': 0,
            'level': level,
            'total_questions': len(questions)
        }
        
        # Return first question
        first_question = questions[0]
        return jsonify({
            'question': first_question['question'],
            'options': first_question['options'],
            'question_number': 1,
            'total_questions': len(questions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check_answer', methods=['POST'])
def check_answer():
    """Check user's answer and return result"""
    try:
        data = request.json
        selected_option = data.get('selected_option')
        
        quiz_data = session.get('quiz')
        if not quiz_data:
            return jsonify({'error': 'No active quiz session'}), 400
        
        current_index = quiz_data['current_index']
        current_question = quiz_data['questions'][current_index]
        
        # Check if answer is correct
        is_correct = (selected_option == current_question['correct'])
        
        if is_correct:
            quiz_data['score'] += 1
        
        # Update session
        session['quiz'] = quiz_data
        
        return jsonify({
            'is_correct': is_correct,
            'correct_answer': current_question['options'][current_question['correct']],
            'explanation': current_question['explanation'],
            'score': quiz_data['score']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/next_question', methods=['POST'])
def next_question():
    """Get the next question or end quiz"""
    try:
        quiz_data = session.get('quiz')
        if not quiz_data:
            return jsonify({'error': 'No active quiz session'}), 400
        
        quiz_data['current_index'] += 1
        current_index = quiz_data['current_index']
        
        # Check if quiz is complete
        if current_index >= len(quiz_data['questions']):
            # Quiz completed
            final_score = quiz_data['score']
            total_questions = len(quiz_data['questions'])
            session.pop('quiz', None)  # Clear quiz session
            return jsonify({
                'quiz_complete': True,
                'final_score': final_score,
                'total_questions': total_questions,
                'percentage': (final_score / total_questions) * 100
            })
        
        # Return next question
        next_question = quiz_data['questions'][current_index]
        return jsonify({
            'question': next_question['question'],
            'options': next_question['options'],
            'question_number': current_index + 1,
            'total_questions': len(quiz_data['questions'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/restart_quiz', methods=['POST'])
def restart_quiz():
    """Clear the quiz session"""
    session.pop('quiz', None)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)