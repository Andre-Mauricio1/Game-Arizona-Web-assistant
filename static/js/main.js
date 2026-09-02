// ============================================
// 1. УВЕДОМЛЕНИЯ (TOAST NOTIFICATIONS)
// ============================================
function showNotification(message, type = 'success') {
    const colors = {
        success: '#238636',
        error: '#da3633',
        warning: '#d29922'
    };

    const existing = document.querySelector('.notification-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'notification-toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: ${colors[type] || '#238636'};
        color: #fff;
        padding: 14px 28px;
        border-radius: 10px;
        font-weight: 500;
        font-size: 0.95rem;
        z-index: 9999;
        box-shadow: 0 8px 30px rgba(0,0,0,0.6);
        animation: slideIn 0.3s ease;
        max-width: 400px;
        word-wrap: break-word;
        border: 1px solid rgba(255,255,255,0.1);
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ============================================
// 2. ОЦЕНКА (КНОПКИ 0 / 0.5 / 1)
// ============================================
let currentScore = null;
const scoreDisplay = document.getElementById('score-display');

document.querySelectorAll('.score-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const score = parseFloat(this.dataset.score);

        document.querySelectorAll('.score-btn').forEach(b => {
            b.style.outline = 'none';
            b.style.boxShadow = 'none';
        });

        this.style.outline = '3px solid #58a6ff';
        this.style.boxShadow = '0 0 15px #58a6ff40';

        currentScore = score;
        if (scoreDisplay) {
            scoreDisplay.textContent = `Оценка: ${score}`;
            scoreDisplay.style.color = '#58a6ff';
        }

        // ОТПРАВЛЯЕМ POST-ЗАПРОС
        const candidate = document.getElementById('current-candidate');
        if (candidate) {
            const candidateName = candidate.textContent;
            fetch('/add_sobes/score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ candidate: candidateName, score: score })
            })
            .then(res => {
                if (!res.ok) throw new Error('Ошибка сервера');
                return res.json();
            })
            .then(() => {
                showNotification(`✅ Оценка ${score} выставлена!`, 'success');
            })
            .catch(err => {
                console.error('❌ Ошибка:', err);
                showNotification('❌ Ошибка при отправке оценки', 'error');
            });
        }
    });
});

// ============================================
// 3. СЛЕДУЮЩИЙ ВОПРОС
// ============================================
const questions = [
    'Что такое деморган?',
    'Какие бывают фракции на сервере?',
    'Что делать при нарушении правил?',
    'Как выдать варн игроку?'
];
let currentQuestionIndex = 0;
const questionText = document.getElementById('question-text');

document.getElementById('next-question')?.addEventListener('click', function () {
    currentQuestionIndex = (currentQuestionIndex + 1) % questions.length;
    if (questionText) {
        questionText.textContent = questions[currentQuestionIndex];
    }

    currentScore = null;
    if (scoreDisplay) {
        scoreDisplay.textContent = 'Оценка: —';
        scoreDisplay.style.color = '#58a6ff';
    }
    document.querySelectorAll('.score-btn').forEach(b => {
        b.style.outline = 'none';
        b.style.boxShadow = 'none';
    });

    showNotification(`📝 Вопрос ${currentQuestionIndex + 1} из ${questions.length}`, 'success');
});

// ============================================
// 4. СЛЕДУЮЩИЙ КАНДИДАТ
// ============================================
const candidates = ['Andre_Mauricio', 'Sebastian_Disney', 'Don_Morrison', 'Test_User'];
let currentCandidateIndex = 0;
const candidateDisplay = document.getElementById('current-candidate');

document.getElementById('next-candidate')?.addEventListener('click', function () {
    currentCandidateIndex = (currentCandidateIndex + 1) % candidates.length;
    if (candidateDisplay) {
        candidateDisplay.textContent = candidates[currentCandidateIndex];
    }

    currentScore = null;
    if (scoreDisplay) {
        scoreDisplay.textContent = 'Оценка: —';
        scoreDisplay.style.color = '#58a6ff';
    }
    document.querySelectorAll('.score-btn').forEach(b => {
        b.style.outline = 'none';
        b.style.boxShadow = 'none';
    });

    showNotification(`👤 Кандидат: ${candidates[currentCandidateIndex]}`, 'success');
});

// ============================================
// 5. ОТМЕНА
// ============================================
document.getElementById('cancel-interview')?.addEventListener('click', function () {
    if (confirm('❌ Отменить собеседование?')) {
        currentScore = null;
        if (scoreDisplay) {
            scoreDisplay.textContent = 'Оценка: —';
        }
        document.querySelectorAll('.score-btn').forEach(b => {
            b.style.outline = 'none';
            b.style.boxShadow = 'none';
        });
        showNotification('❌ Собеседование отменено', 'warning');
    }
});

// ============================================
// 6. ЗАВЕРШИТЬ СОБЕСЕДОВАНИЕ
// ============================================
document.getElementById('finish-interview')?.addEventListener('click', function () {
    if (currentScore === null) {
        showNotification('⚠️ Сначала выставьте оценку!', 'warning');
        return;
    }

    const candidate = candidateDisplay ? candidateDisplay.textContent : 'Неизвестно';
    if (confirm(`✅ Завершить собеседование для ${candidate}?`)) {
        showNotification(`✅ Собеседование завершено! Оценка: ${currentScore}`, 'success');

        currentScore = null;
        if (scoreDisplay) {
            scoreDisplay.textContent = 'Оценка: —';
        }
        document.querySelectorAll('.score-btn').forEach(b => {
            b.style.outline = 'none';
            b.style.boxShadow = 'none';
        });
    }
});

// ============================================
// 7. ДОБАВЛЕНИЕ КАНДИДАТА (POST)
// ============================================
document.querySelector('.interview-form')?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const form = this;
    const formData = new FormData(form);
    const username = formData.get('username');

    if (!username.trim()) return;

    try {
        const res = await fetch(form.action, {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Ошибка сервера');
        }

        const user = await res.json();

        const tbody = document.getElementById('candidates-body');
        const row = document.createElement('tr');
        const now = new Date().toLocaleString();
        const newId = tbody ? tbody.children.length + 1 : 1;

        row.innerHTML = `
            <td>${newId}</td>
            <td>${user.username || username}</td>
            <td>—</td>
            <td>—</td>
            <td>${now}</td>
            <td class="score-cell">—</td>
            <td><span class="status-badge status-waiting">⏳ Ожидает</span></td>
            <td>
                <button class="action-btn edit-btn" data-id="${newId}" data-action="edit">✏️</button>
                <button class="action-btn danger" data-id="${newId}" data-action="delete">🗑️</button>
            </td>
        `;

        if (tbody) tbody.appendChild(row);
        form.querySelector('input[name="username"]').value = '';

        showNotification('✅ Кандидат добавлен!', 'success');

    } catch (err) {
        console.error(err);
        showNotification('❌ Ошибка при добавлении: ' + err.message, 'error');
    }
});

// ============================================
// 8. РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ (PATCH / DELETE)
// ============================================
document.getElementById('candidates-body')?.addEventListener('click', async function (e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const id = btn.dataset.id;
    const action = btn.dataset.action;
    const row = btn.closest('tr');

    // УДАЛЕНИЕ
    if (action === 'delete') {
        if (!confirm('Удалить кандидата?')) return;

        try {
            const res = await fetch(`/add_sobes/users/${id}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Ошибка удаления');
            }

            row.remove();
            showNotification('🗑️ Кандидат удалён', 'success');

        } catch (err) {
            console.error(err);
            showNotification('❌ Ошибка при удалении: ' + err.message, 'error');
        }
    }

    // РЕДАКТИРОВАНИЕ
    if (action === 'edit') {
        const cells = row.querySelectorAll('td');
        const currentName = cells[1].textContent.trim();

        const newName = prompt('Введите новый никнейм:', currentName);
        if (!newName || newName === currentName) return;

        try {
            const res = await fetch(`/add_sobes/users/${id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: newName })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Ошибка редактирования');
            }

            cells[1].textContent = newName;
            showNotification('✅ Никнейм обновлён!', 'success');

        } catch (err) {
            console.error(err);
            showNotification('❌ Ошибка при редактировании: ' + err.message, 'error');
        }
    }
});

// ============================================
// 9. CSS ДЛЯ АНИМАЦИИ
// ============================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .action-btn {
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .action-btn:hover {
        transform: scale(1.05);
    }
    .action-btn:active {
        transform: scale(0.95);
    }
    .score-btn {
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .score-btn:hover {
        transform: scale(1.08);
    }
    .score-btn:active {
        transform: scale(0.95);
    }
`;
document.head.appendChild(style);