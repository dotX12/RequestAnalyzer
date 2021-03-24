from pygooglechart import PieChart2D

def create_diagram_requests(count_bad, count_good):
    chart = PieChart2D(650, 300)
    chart.set_title('HTTP Requests')
    chart.add_data([count_good, count_bad])
    chart.set_pie_labels(["Bad Requests", "Good Requests"])
    chart.set_legend([f'Count XSS, SQL INJ Requests - {count_good}',
                      f'Good Requests - {count_bad}'])
    chart.set_colours(['8e5ea2', '3e95cd'])
    url = chart.get_url()
    return url
