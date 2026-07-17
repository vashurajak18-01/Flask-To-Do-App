from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)


# View All Tasks
@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


# Add New Task
@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')

    if title:
        new_task = Task(title=title, status='Pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')

    return redirect(url_for('tasks.view_tasks'))


# Change Task Status
@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    task = db.session.get(Task, task_id)

    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'

        db.session.commit()

    return redirect(url_for('tasks.view_tasks'))


# Delete One Task
@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    task = db.session.get(Task, task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')

    return redirect(url_for('tasks.view_tasks'))


# Clear All Tasks
@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')

    return redirect(url_for('tasks.view_tasks'))