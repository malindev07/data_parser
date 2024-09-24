from pymongo import MongoClient
import matplotlib.pyplot as plt
import mpld3
import webbrowser


async def get_prices(topic: str, title: str) -> list:
    client = MongoClient("mongodb://mongodb:27017/")
    # client = MongoClient("mongodb://localhost:27017/")
    db = client["parser_db"]
    collection = db[f"{topic}.{title}"]
    all_data = collection.find()

    old_prices: list[int] = []
    dates: list = []
    for item in all_data:

        old_prices.append(int(item["old_price"]))
        dates.append(item["date_time"])

    res = [old_prices, dates]
    print(old_prices)
    return res


async def create_plot(topic: str, title: str, prices: list):

    fig1, ax1 = plt.subplots()
    ax1.plot(prices[1], prices[0], "ro")
    ax1.set_xlabel("")
    ax1.set_ylabel("Price")

    html_fig1 = mpld3.fig_to_html(fig1)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{topic + " " + title}</title>
    </head>
    <body>
        <h1>{topic + " " + title}</h1>
        {html_fig1}

    </body>
    </html>
    """

    with open("matplotlib_figures.html", "w") as f:
        f.write(html_content)

    webbrowser.open_new_tab("matplotlib_figures.html")
