import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_hist(data, column_name, title):
    # Chuyển QuerySet thành list để truy cập theo chỉ số
    data_list = list(data.values_list(column_name, flat=True))
    
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))

    # Vẽ biểu đồ bằng matplotlib
    plt.subplot(1, 2, 1)  # Biểu đồ 1
    plt.hist(data_list, bins=8)
    plt.title(f'{title} - Matplotlib')

    # Vẽ biểu đồ bằng seaborn
    plt.subplot(1, 2, 2)  # Biểu đồ 2
    sns.histplot(data_list, bins=8)
    plt.title(f'{title} - Seaborn')

    plt.tight_layout()  # Đảm bảo khoảng cách giữa các biểu đồ
    graph = get_graph()  # Lấy đối tượng hình ảnh để render

    return graph