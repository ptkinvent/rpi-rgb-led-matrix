#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from weather_client import WeatherClient
import time
import datetime

class TestClient:
    def query_weather(self):
        pass

    def get_current_temperature(self):
        return "50"

    def get_low_temperature(self):
        return "47"

    def get_high_temperature(self):
        return "53"

    def get_description(self):
        return "Clear sky"

    def get_air_quality_index(self):
        return 1


class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        brightness = 1
        self.white = graphics.Color(255*brightness, 255*brightness, 255*brightness)
        self.gray = graphics.Color(150*brightness, 150*brightness, 150*brightness)
        self.red = graphics.Color(255*brightness, 0, 0)
        self.blue = graphics.Color(0, 0, 255*brightness)

        # TODO: Use some color library.
        self.green = graphics.Color(0, 127*brightness, 0);
        self.yellow = graphics.Color(255*brightness, 255*brightness, 0);
        self.orange = graphics.Color(255*brightness, 165*brightness, 0);
        self.purple = graphics.Color(128*brightness, 0, 128*brightness);

    def run(self):
        canvas = self.matrix
        font_h1 = graphics.Font()
        font_h1.LoadFont("../../../fonts/9x18.bdf")
        font_h2 = graphics.Font()
        font_h2.LoadFont("../../../fonts/6x10.bdf")
        font_h3 = graphics.Font()
        font_h3.LoadFont("../../../fonts/5x7.bdf")

        client = WeatherClient()
        #client = TestClient()

        while True:
            client.query_weather()
            curr_temp = client.get_current_temperature() + '°F'
            low_temp = client.get_low_temperature()
            high_temp = client.get_high_temperature()
            desc = client.get_description()
            aqi = client.get_air_quality_index()

            # TODO: Move this inner method to somewhere more appropriate.
            def parse_aqi_color(aqi):
                colors = [self.green, self.yellow, self.orange, self.red, self.purple]
                return colors[aqi-1]

            def parse_aqi_text(aqi):
                text = ['Good', 'Fair', 'Moderate', 'Poor', 'Very poor']
                return text[aqi-1]

            aqi_color = parse_aqi_color(aqi)
            aqi_text = parse_aqi_text(aqi)

            print(time.time(), curr_temp, low_temp, high_temp, '\n')

            canvas.Clear()

            graphics.DrawText(canvas, font_h2, 2, 10, self.gray, desc)
            graphics.DrawText(canvas, font_h2, 2, 21, aqi_color, f'AQI: {aqi_text}')

            # Draw weather
            graphics.DrawText(canvas, font_h1, 15, 40, self.white, curr_temp)
            graphics.DrawText(canvas, font_h2, 18, 51, self.red, high_temp)
            graphics.DrawText(canvas, font_h2, 35, 51, self.blue, low_temp)

            # Draw date/time
            time_str = datetime.datetime.now().strftime('%-I:%M')
            date_str = datetime.datetime.now().strftime('%-m/%-d')
            num_chars_width = 11
            num_chars_remaining = num_chars_width - len(time_str) - len(date_str)
            time_x = 1
            date_x = time_x + 6*len(time_str) + 6*num_chars_remaining
            graphics.DrawText(canvas, font_h3, time_x, 63, self.gray, time_str)
            graphics.DrawText(canvas, font_h3, date_x, 63, self.gray, date_str)

            time.sleep(60)


# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
