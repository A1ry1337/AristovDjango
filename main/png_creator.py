import matplotlib.pyplot as plt
import seaborn as sns


# Динамика по словарю(ключ - значение например 'год - кол-во вакансий')
def plot_dynamics(average_salary_dynamics, output_filename, x_label, y_label):
    # Используем стиль seaborn-dark для темной цветовой схемы
    sns.set(style="darkgrid")

    years = list(average_salary_dynamics.keys())
    avg_salaries = list(average_salary_dynamics.values())

    # Настраиваем цвета линии
    line_color = '#00ff00'  # Лайм цвет

    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_salaries, marker='o', color=line_color)
    plt.title(label='', color='white', fontname='Arial')  # Установка шрифта для заголовка
    plt.xlabel(x_label, color='white', fontname='Arial')  # Установка шрифта для оси X
    plt.ylabel(y_label, color='white', fontname='Arial')  # Установка шрифта для оси Y
    plt.tick_params(axis='x', colors='white', labelsize=10)  # Цвет и размер делений оси X
    plt.tick_params(axis='y', colors='white', labelsize=10)  # Цвет и размер делений оси Y
    plt.grid(True, color='white', linestyle='--', alpha=0.5)  # Цвет сетки и ее стиль

    # Настраиваем прозрачный фон
    plt.gca().set_facecolor('none')
    plt.gcf().set_facecolor('none')
    plt.gca().xaxis.label.set_color('white')
    plt.gca().yaxis.label.set_color('white')

    # Сохраняем график с прозрачным фоном
    plt.savefig(output_filename, format='png', bbox_inches='tight', transparent=True)
    plt.close()


def plot_table_dynamics(data_dict, file_name):
    # Создаем изображение с прозрачным фоном
    fig, ax = plt.subplots(figsize=(8, 1))
    ax.axis('off')

    # Устанавливаем размер шрифта
    font_size = 18

    # Устанавливаем фиксированный размер рамки
    bbox_props = dict(facecolor='none', edgecolor='#00ff00', boxstyle='round', linewidth=2)

    # Создаем таблицу с использованием ax.text
    for i, (key, value) in enumerate(data_dict.items()):
        ax.text(i * 0.2, 0.8, f'{key}\n{int(value)}', ha='center', va='center', fontfamily='monospace',
                color='#00ff00', fontsize=font_size, bbox=bbox_props)

    # Сохраняем изображение с фиксированным расстоянием между рамками
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.1, transparent=True)

    # Очищаем график
    plt.close()
