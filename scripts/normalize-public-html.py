from pathlib import Path


def normalize(root: Path) -> None:
    for path in root.rglob('*.html'):
        # Google Search Console verification files must remain byte-for-byte compatible.
        if path.name == 'google7cf685e23093cfe7.html':
            continue
        html = path.read_text(encoding='utf-8')

        # Keep both stable fragments: #search for library search and #quick-revision for flashcards.
        html = html.replace(
            '<section id="quick-revision" class="search-panel">',
            '<section id="search" class="search-panel"><span id="quick-revision" aria-hidden="true"></span>'
        )

        # Stable homepage persona anchors used by the plant dossier navigation.
        html = html.replace(
            '<article class="persona"><div class="icon">🎓</div><h3>Student',
            '<article id="student" class="persona"><div class="icon">🎓</div><h3>Student'
        )
        html = html.replace(
            '<article class="persona"><div class="icon">👨‍🏫</div><h3>Teacher',
            '<article id="teacher" class="persona"><div class="icon">👨‍🏫</div><h3>Teacher'
        )
        html = html.replace(
            '<article class="persona"><div class="icon">🩺</div><h3>Doctor',
            '<article id="doctor" class="persona"><div class="icon">🩺</div><h3>Doctor'
        )

        # Make the progress indicator accessible and valid ARIA.
        html = html.replace(
            '<div class="progress-track" aria-label="Study progress">',
            '<div class="progress-track" role="progressbar" aria-label="Study progress" aria-valuemin="0" aria-valuemax="97" aria-valuenow="0">'
        )
        # The filter row is a generic layout container, not a labelled ARIA widget.
        html = html.replace(
            '<div class="filter-row" aria-label="Dravyaguna filters">',
            '<div class="filter-row">'
        )

        # Give the dynamically populated modal image a valid initial source.
        html = html.replace(
            '<img id="modal-img" alt="Expanded plant image">',
            '<img id="modal-img" src="images/favicon.png" alt="Expanded plant image">'
        )

        path.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    normalize(Path('.'))
