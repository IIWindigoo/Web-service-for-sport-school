document.addEventListener('DOMContentLoaded', function() {    
    // Обработка удаления тренировки (аналогично)
    document.querySelectorAll('.delete-training').forEach(btn => {
        btn.addEventListener('click', async function() {
            const trainingId = this.dataset.trainingId;
            if (confirm(`Вы уверены, что хотите удалить тренировку ID: ${trainingId}?`)) {
                try {
                    const response = await fetch(`/trainings/${trainingId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        }
                    });
                    
                    if (response.ok) {
                        showToast('success', 'Тренировка успешно удалена');
                        this.closest('tr').remove();
                    } else {
                        const error = await response.json();
                        showToast('error', error.detail || 'Ошибка при удалении тренировки');
                    }
                } catch (error) {
                    console.error('Ошибка:', error);
                    showToast('error', 'Произошла ошибка. Попробуйте позже.');
                }
            }
        });
    });
});

function showToast(type, message) {
    const toastContainer = document.getElementById('toastContainer');
    const toastEl = document.createElement('div');
    toastEl.className = `toast show align-items-center text-white bg-${type}`;
    toastEl.setAttribute('role', 'alert');
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    toastContainer.appendChild(toastEl);
    setTimeout(() => toastEl.remove(), 5000);
}

// Функция для обновления роли
async function updateRole(userId, newRole) {
    if (!confirm(`Вы уверены, что хотите изменить роль пользователя ${userId} на ${newRole}?`)) {
      return;
    }
  
    try {
      const response = await fetch(`/user/${userId}/role`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({ new_role: newRole })
      });
  
      const result = await response.json();
      
      if (response.ok) {
        showToast('success', result.message);
        // Обновляем кнопку dropdown
        const dropdownBtn = document.querySelector(`#roleDropdown${userId}`);
        dropdownBtn.textContent = newRole;
      } else {
        showToast('error', result.detail || 'Ошибка при изменении роли');
      }
    } catch (error) {
      console.error('Ошибка:', error);
      showToast('error', 'Произошла ошибка. Попробуйте позже.');
    }
  }
  
  // Инициализация dropdown после загрузки страницы
  document.addEventListener('DOMContentLoaded', function() {
    // Инициализируем все dropdown элементы
    var dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(function(dropdown) {
      dropdown.addEventListener('click', function(e) {
        e.preventDefault();
        var dropdownMenu = this.nextElementSibling;
        dropdownMenu.classList.toggle('show');
      });
    });
  
    // Закрываем dropdown при клике вне его
    document.addEventListener('click', function(e) {
      if (!e.target.matches('.dropdown-toggle') && !e.target.matches('.dropdown-item')) {
        var dropdowns = document.querySelectorAll('.dropdown-menu');
        dropdowns.forEach(function(dropdown) {
          dropdown.classList.remove('show');
        });
      }
    });
  });