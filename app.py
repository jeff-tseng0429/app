from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, ToDo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 初始化数据库
with app.app_context():
    db.create_all()

# 显示待办事项列表
@app.route('/')
def index():
    todos = ToDo.query.all()
    return render_template('index.html', todos=todos)

# 显示新增待办事项页面
@app.route('/create')
def create_page():
    return render_template('create.html')

# 新增待办事项 API
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = ToDo(
        title=data['title'],
        time=data['time'],
        content=data['content']
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# 获取单篇待办事项 API
@app.route('/api/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = ToDo.query.get_or_404(id)
    return jsonify(todo.to_dict())

# 更新待办事项 API
@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.json
    todo = ToDo.query.get_or_404(id)
    todo.title = data['title']
    todo.time = data['time']
    todo.content = data['content']
    db.session.commit()
    return jsonify(todo.to_dict())

# 删除待办事项 API
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = ToDo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'To-Do deleted successfully'})

# 显示单篇待办事项页面
@app.route('/todos/<int:id>')
def todo_detail(id):
    todo = ToDo.query.get_or_404(id)
    return render_template('detail.html', todo=todo)

# 显示编辑待办事项页面
@app.route('/todos/<int:id>/edit')
def edit_page(id):
    todo = ToDo.query.get_or_404(id)
    return render_template('edit.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



