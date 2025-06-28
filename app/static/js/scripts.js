document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch("/user/login/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    const error = await response.json();
                    alert(error.detail || "Ошибка авторизации");
                    return;
                }

                const result = await response.json();

                if (result.ok) {
                    location.reload(); // Перезагрузим страницу для показа личного кабинета
                } else {
                    alert(result.message || "Неизвестная ошибка");
                }
            } catch (err) {
                console.error("Ошибка запроса:", err);
                alert("Сервер временно недоступен.");
            }
        });
    }
});

async function logoutFunction() {
    try {
      const response = await fetch('/user/logout/', {
        method: 'POST',
      });
  
      const result = await response.json();
  
      if (response.ok) {
        //alert(result.message); // по желанию
        window.location.href = "/page/";  // возвращаем на главную
      } else {
        alert("Ошибка при выходе: " + (result.message || "неизвестно"));
      }
    } catch (error) {
      console.error("Ошибка при выходе:", error);
      alert("Сервер недоступен");
    }
  }

async function regFunction(event) {
    event.preventDefault();
  
    const form = document.getElementById('registration-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    console.log("Данные для отправки:", data);

    // Валидация паролей
    if (data.password !== data.confirm_password) {
      alert("Пароли не совпадают!");
      return;
    }
  
    try {
      const response = await fetch('/user/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
  
      const result = await response.json();
  
      if (!response.ok) {
        displayErrors(result);
        return;
      }
  
      alert(result.message || "Регистрация успешна");
      const modal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
      modal.hide();
  
      // Очищаем форму
      form.reset();
  
      // Переход на логин или автооткрытие окна входа
      const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
      loginModal.show();
  
    } catch (error) {
      console.error("Ошибка:", error);
      alert("Ошибка регистрации. Попробуйте позже.");
    }
  }

function displayErrors(errorData) {
    let message = 'Произошла ошибка';
    if (errorData && errorData.detail) {
      if (Array.isArray(errorData.detail)) {
        message = errorData.detail.map(e => e.msg || e.detail || "Ошибка").join('\n');
      } else {
        message = errorData.detail;
      }
    }
    alert(message);
  }

  async function cancelBooking(trainingId) {
    console.log("Starting cancellation for:", trainingId);
    if (!confirm('Вы уверены, что хотите отменить запись?')) return;
    
    try {
        const response = await fetch('/bookings/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`
            },
            body: JSON.stringify({ training_id: parseInt(trainingId) })
        });

        console.log("Response status:", response.status);
        
        if (response.status === 204) {
            alert('Запись отменена!');
            location.reload();
        } else {
            const error = await response.json();
            alert(error.detail || 'Ошибка при отмене');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка сети');
    }
}

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, initializing buttons...");
    
    document.querySelectorAll('.cancel-booking').forEach(btn => {
        btn.addEventListener('click', function() {
            const trainingId = this.getAttribute('data-training-id');
            console.log("Button click detected, ID:", trainingId);
            cancelBooking(trainingId);
        });
    });
});

// Функция для показа уведомлений (добавьте её если ещё нет)
function showToast(type, message) {
    const toastContainer = document.getElementById('toastContainer') || document.body;
    const toastEl = document.createElement('div');
    toastEl.className = `toast show align-items-center text-white bg-${type} border-0`;
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

  function editProfile() {
    // Здесь можно реализовать редактирование профиля
    alert('Функция редактирования профиля будет реализована позже');
  }

  // Функция для записи на тренировку
async function bookTraining(trainingId) {
    try {
        const response = await fetch('/bookings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({
                training_id: trainingId
            })
        });

        if (response.ok) {
            const result = await response.json();
            alert('Вы успешно записаны на тренировку!');
            // Можно обновить страницу или изменить состояние кнопки
            window.location.reload();
        } else {
            const error = await response.json();
            handleBookingError(error);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при записи. Попробуйте позже.');
    }
}

// Обработчик ошибок при записи
function handleBookingError(error) {
    let message = 'Ошибка при записи';
    
    if (error.detail) {
        if (typeof error.detail === 'string') {
            message = error.detail;
        } else if (Array.isArray(error.detail)) {
            message = error.detail.map(e => e.msg || e.detail).join('\n');
        }
    }
    
    alert(message);
}

// Инициализация обработчиков после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для кнопок записи
    document.querySelectorAll('.book-training').forEach(button => {
        button.addEventListener('click', function() {
            const trainingId = this.getAttribute('data-training-id');
            if (confirm(`Вы уверены, что хотите записаться на эту тренировку?`)) {
                bookTraining(trainingId);
            }
        });
    });
});

// Функция для создания тренировки
async function createTraining(event) {
    event.preventDefault();
    
    const form = document.getElementById('create-training-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Преобразуем дату и время в правильный формат
    data.date = new Date(data.date).toISOString().split('T')[0];
    
    try {
        const response = await fetch('/trainings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            alert('Тренировка успешно создана!');
            // Закрываем модальное окно
            const modal = bootstrap.Modal.getInstance(document.getElementById('createTrainingModal'));
            modal.hide();
            // Обновляем страницу
            window.location.reload();
        } else {
            const error = await response.json();
            alert(error.detail || 'Ошибка при создании тренировки');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Попробуйте позже.');
    }
}

// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create-training-form');
    if (form) {
        form.addEventListener('submit', createTraining);
    }
    
    // Установка минимальной даты (сегодня)
    const dateInput = document.querySelector('input[name="date"]');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
});

// Обработчик кнопки редактирования
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация модального окна редактирования
    document.querySelectorAll('.edit-training').forEach(button => {
        button.addEventListener('click', function() {
            const modal = document.getElementById('editTrainingModal');
            modal.querySelector('#edit-training-id').value = this.dataset.trainingId;
            modal.querySelector('#edit-training-title').value = this.dataset.trainingTitle;
            modal.querySelector('#edit-training-description').value = this.dataset.trainingDescription;
            modal.querySelector('#edit-training-date').value = this.dataset.trainingDate;
            modal.querySelector('#edit-training-start-time').value = this.dataset.trainingStartTime;
            modal.querySelector('#edit-training-end-time').value = this.dataset.trainingEndTime;
        });
    });

    // Обработчик формы редактирования
    const editForm = document.getElementById('edit-training-form');
    if (editForm) {
        editForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(editForm);
            const trainingId = formData.get('id');
            const data = {
                title: formData.get('title'),
                description: formData.get('description'),
                date: formData.get('date'),
                start_time: formData.get('start_time'),
                end_time: formData.get('end_time')
            };

            try {
                const response = await fetch(`/trainings/${trainingId}/`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    alert('Тренировка успешно обновлена!');
                    window.location.reload();
                } else {
                    const error = await response.json();
                    alert(error.detail || 'Ошибка при обновлении тренировки');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка. Попробуйте позже.');
            }
        });
    }

    // Обработчик удаления тренировки
    document.querySelectorAll('.delete-training').forEach(button => {
        button.addEventListener('click', async function() {
            const trainingId = this.dataset.trainingId;
            if (!confirm('Вы уверены, что хотите удалить эту тренировку?')) return;

            try {
                const response = await fetch(`/trainings/${trainingId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });

                if (response.ok) {
                    alert('Тренировка успешно удалена!');
                    window.location.reload();
                } else {
                    const error = await response.json();
                    alert(error.detail || 'Ошибка при удалении тренировки');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка. Попробуйте позже.');
            }
        });
    });
});