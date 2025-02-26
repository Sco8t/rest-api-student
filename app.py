from flask import Flask, jsonify, request, abort

app = Flask(__name__)

students = [
    {"id": 1, "name": "Alice", "grade": "A", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "grade": "B", "email": "bob@example.com"},
]

@app.route('/')
def index():
    return "Welcome to the Student API! Try accessing /students to see all students."

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((student for student in students if student['id'] == student_id), None)
    if student is None:
        abort(404)
    return jsonify(student), 200

@app.route('/students', methods=['POST'])
def create_student():
    if not request.json or not 'name' in request.json:
        abort(400)
    new_student = {
        'id': students[-1]['id'] + 1 if students else 1,
        'name': request.json['name'],
        'grade': request.json.get('grade', 'N/A'),
        'email': request.json.get('email', 'N/A')
    }
    students.append(new_student)
    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((student for student in students if student['id'] == student_id), None)
    if student is None:
        abort(404)
    if not request.json:
        abort(400)
    student['name'] = request.json.get('name', student['name'])
    student['grade'] = request.json.get('grade', student['grade'])
    student['email'] = request.json.get('email', student['email'])
    return jsonify(student), 200

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [student for student in students if student['id'] != student_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)