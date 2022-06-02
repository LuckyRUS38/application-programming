import random
import cfg
import SQLConnect as sql
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/cats', methods=['GET'])
def index():
    data = dict(request.args)
    if 'color' not in data:
        return render_template('cats.html')
    color = data['color']
    if color not in ('black', 'white', 'orange', 'all'):
        return render_template('404.html'), 404
    html_text = ''
    file_name_list = []
    if color == 'all':
        file_name_list = sql.get_photos(999999999, '', True)
    else:
        file_name_list = sql.get_photos(999999999, color, True)

    for file_name in file_name_list:
        html_text += """
            <tr>
                <td class="firstColumn>
                    <img src=%s>
                </td>
                <td class="secondColumn>
                    %s
                </td>
                <td class="thirdColumn>
                    %s
                </td>
        """ % (cfg.image_host + file_name[0], file_name[1], file_name[2])

    headers = {'all': 'Коты всех цветов', 'white': 'Белые коты', 'orange': 'Оранжевые коты', 'black': 'Чёрные коты'}
    return render_template('pictures.html', title=headers[color], table=html_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0")