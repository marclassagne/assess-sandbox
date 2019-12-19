import io
import matplotlib.pyplot as plt
import base64


def render(formula):
    """Renders LaTeX formula into image.
    """
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, r'${}$'.format(formula), fontsize=4)
    imgdata = io.BytesIO()
    fig.savefig(imgdata, dpi=300, transparent=True, format='png',
                bbox_inches='tight', pad_inches=0.0)
    imgdata = base64.b64encode(imgdata.getvalue())
    return imgdata
