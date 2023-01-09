import plotly
import plotly.graph_objs as go 

def get_figures(frame,r):
    fig = go.Figure()
    fig = plotly.subplots.make_subplots(rows=3, cols=1, shared_xaxes=True,
    vertical_spacing=0.01, row_heights=[0.5,0.2,0.2])
    fig.add_trace(go.Candlestick(x=frame['Date'].tail(r), open=frame['Open'].tail(r), high=frame['High'].tail(r), low=frame['Low'].tail(r), close=frame['Close'].tail(r)))
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r), 
         y=frame['EMA20'].tail(r), 
         opacity=0.7, 
         line=dict(color='green', width=2), 
         name='EMA 20'))
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r), 
         y=frame['EMA50'].tail(r), 
         opacity=0.7, 
         line=dict(color='orange', width=2), 
         name='EMA 50'))
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r), 
         y=frame['EMA200'].tail(r), 
         opacity=0.7, 
         line=dict(color='blue', width=2), 
         name='EMA 200'))
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r), 
         y=frame['sup2'].tail(r),
         opacity=0.7,
         mode='markers', marker=dict(size=3,color='green'), 
         name='Supertrend1'))
    fig.add_trace(go.Scatter(x=framew['Date'].tail(3), 
         y=framew['sup2'].tail(3),
         opacity=0.7,
         mode='markers', marker=dict(size=3,color='red'), 
         name='Supertrend1'))
    fig.add_trace(go.Scatter(x=framew['Date'].tail(3), 
         y=framew['sup4'].tail(3),
         opacity=0.7,
         mode='markers', marker=dict(size=3,color='red'), 
         name='Supertrend2'))
    fig.add_trace(go.Scatter(x=framew['Date'].tail(3), 
         y=framew['sup6'].tail(3),
         opacity=0.7,
         mode='markers', marker=dict(size=3,color='red'), 
         name='Supertrend3'))
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r), 
         y=frame['sup4'].tail(r),
         opacity=0.7,
         mode='markers', marker=dict(size=3,color='orange'), 
         name='Supertrend2'))
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r), 
         y=frame['sup6'].tail(r),
         opacity=0.7,
         mode='markers', marker=dict(size=3,color='blue'), 
         name='Supertrend3'))
    fig.add_trace(go.Bar(x=frame['Date'].tail(r), 
     y=frame['MACD_diff'].tail(r)
        ), row=2, col=1)
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r),
         y=frame['MACD'].tail(r),
         line=dict(color='blue', width=1)
        ), row=2, col=1)
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r),
         y=frame['MACD_signal'].tail(r),
         line=dict(color='orange', width=1)
        ), row=2, col=1)
    
    fig.add_trace(go.Bar(x=frame['Date'].tail(r), 
     y=frame['Volume'].tail(r)
        ), row=3, col=1)
    fig.add_trace(go.Scatter(x=frame['Date'].tail(r),
         y=frame['Volume_EMA'].tail(r),
         line=dict(color='orange', width=2)
        ), row=3, col=1)
    fig.update_layout( height=600, width=1200,
        showlegend=False, xaxis_rangeslider_visible=False)
    return fig


def expander(cond):
       with st.expander(cond+' '+str(sira) +') '+ name+'/'+' RISK= '+str(frame['RISK'].iloc[-1].round(2))+'/ %ATR='+str(frame['ATR%'].iloc[-1].round(2))+'/ %wATR='+str(framew['ATR%'].iloc[-1].round(2))):
           #st.write(str(sira) +') '+ name+'/'+' RISK= '+str(frame['RISK'].iloc[-1].round(2))+'/ %ATR='+str(frame['ATR%'].iloc[-1].round(2)))
           #col6, col3, col4 = st.columns([1, 1, 1])
           col3, col4 = st.columns([1, 1])
           col3.write(frame[['Close','ATR%','ADX','EMA20_cross','EMA50_cross','Decision Super','Decision Super2','Decision Super3','Dec_MACD','Trend MACD','MACD_diff']].tail(2))
           col4.write(framew[['Close','ATR%','ADX','EMA20_cross','EMA50_cross','Decision Super','Decision Super2','Decision Super3','Dec_MACD','Trend MACD','MACD_diff']].tail(2))
           #col6.write(frameh[['Close','ATR%','ADX','Dec_EMA50','Dec_MACD','Trend MACD','MACD_diff']].tail(2))
           #col5, col1, col2 = st.columns([1, 1, 1])
           col1, col2 = st.columns([1, 1])
           r=100
           fig=get_figures(frame,r)
           r=40
           figw=get_figures(framew,r)
           r=300      
           col1.plotly_chart(fig,use_container_width=True)
           col2.plotly_chart(figw,use_container_width=True)
