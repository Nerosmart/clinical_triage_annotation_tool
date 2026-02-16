const streamlit = window.parent.Streamlit;

function sendSelection() {
    const selection = window.getSelection();
    const text = selection.toString();

    if (!text) {
        streamlit.setComponentValue(null);
        return;
    }

    const range = selection.getRangeAt(0);
    const start = range.startOffset;
    const end = range.endOffset;

    streamlit.setComponentValue({
        text: text,
        start: start,
        end: end
    });
}

document.addEventListener("mouseup", sendSelection);
document.addEventListener("keyup", sendSelection);

window.addEventListener("load", () => {
    streamlit.setFrameHeight(document.body.scrollHeight);
});