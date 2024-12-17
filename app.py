import reflex as rx
import json

# Load stock data
with open("stocks.json", "r") as f:
    STOCKS = json.load(f)

# Define the app state
class StockState(rx.State):
    current_page: int = 0  # Tracks the current stock page

    @property
    def current_stock(self):
        return STOCKS[self.current_page]

    @property
    def has_next(self):
        return self.current_page < len(STOCKS) - 1

    @property
    def has_prev(self):
        return self.current_page > 0

    def next_page(self):
        if self.has_next:
            self.current_page += 1

    def prev_page(self):
        if self.has_prev:
            self.current_page -= 1


# TradingView Widget Component
def tradingview_chart(symbol: str):
    return rx.box(
        rx.html(
            f"""
            <div class="tradingview-widget-container">
                <div id="tradingview_chart"></div>
                <script type="text/javascript">
                    new TradingView.widget({{
                        "container_id": "tradingview_chart",
                        "symbol": "BSE:{symbol}",
                        "theme": "light",
                        "style": "1",
                        "locale": "en",
                        "toolbar_bg": "#f1f3f6",
                        "enable_publishing": false,
                        "hide_top_toolbar": true,
                        "width": "100%",
                        "height": "500px"
                    }});
                </script>
            </div>
            """
        ),
        style={"width": "100%", "margin": "auto"},
    )


# App Layout
def index():
    return rx.center(
        rx.vstack(
            rx.heading("Top 50 Indian Stocks", size="lg", margin_bottom="2rem"),
            rx.box(
                rx.text(
                    f"Current Stock: {StockState.current_stock['name']} ({StockState.current_stock['symbol']})",
                    size="md",
                ),
                margin_bottom="1rem",
            ),
            tradingview_chart(StockState.current_stock["symbol"]),
            rx.hstack(
                rx.button("Previous", on_click=StockState.prev_page, disabled=~StockState.has_prev),
                rx.button("Next", on_click=StockState.next_page, disabled=~StockState.has_next),
                spacing="1rem",
                margin_top="1rem",
            ),
            spacing="2rem",
        ),
        padding="2rem",
        style={"max_width": "900px", "width": "100%", "margin": "auto"},
    )


# Add the page
app = rx.App()
app.add_page(index)
app.compile()
