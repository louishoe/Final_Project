# weather_description

def icons(df, weather_col):
     from skimage import io
     import pandas as pd
     import pandas as pd
     import numpy as np
    
     if df[weather_col].iloc[0] == "clear sky":
          img = io.imread('./assets/images/{icon}'.format(icon='sunny.jpg'))
     elif df[weather_col].iloc[0] == "few clouds":
          img = io.imread('./assets/images/{icon}'.format(icon='overcast.png'))
     elif "clouds" in df[weather_col].iloc[0]:
          img = io.imread('./assets/images/{icon}'.format(icon='cloudy.png'))
     elif df[weather_col].iloc[0] == "snow":
          img = io.imread('./assets/images/{icon}'.format(icon='snow.png'))
     elif df[weather_col].iloc[0] == "drizzle":
          img = io.imread('./assets/images/{icon}'.format(icon='drizzle.png'))
     elif "rain" in df[weather_col].iloc[0]:
          img = io.imread('./assets/images/{icon}'.format(icon='raining2.png'))
     elif df[weather_col].iloc[0] == "thunderstorm":
          img = io.imread('./assets/images/{icon}'.format(icon='thunderstorm.png'))
     elif df[weather_col].iloc[0] == "mist":
          img = io.imread('./assets/images/{icon}'.format(icon='mist.png'))
     else:
          img = io.imread('./assets/images/{icon}'.format(icon='question.png'))
     
     fig = px.imshow(img)
     fig.update_xaxes(showticklabels=False)
     fig.update_yaxes(showticklabels=False)
     
     return fig