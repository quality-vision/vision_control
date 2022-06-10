import random

RESERVED_COLORS = {
    "sentry": "e1567c",
    "gitlab": "fca326",
    "loki": "ffae4f",
    "prometheus": "df4f2b",
}


def define_env(env):
    @env.macro
    def render_tags(tags):
        def tag_html(tag):
            color = RESERVED_COLORS.get(tag.lower())

            if not color:
                blend = (210, 120, 150)
                red = int((random.randint(0, 255) + blend[0]) / 2)
                green = int((random.randint(0, 255) + blend[1]) / 2)
                blue = int((random.randint(0, 255) + blend[2]) / 2)

                color = f"{hex(red)[2:4]}{hex(green)[2:4]}{hex(blue)[2:4]}"

            return f'<a href="{ env.conf["site_url"] }search.html?q={tag}"><span style="font-size: 15px; background-color: #{color}; padding: 2px 3px; border-radius: 3px; margin: 1.5px 1.5px 1.5px 1.5px; color: white;">{tag}</span></a>'

        html = ""
        special_tags = [tag for tag in tags if tag in RESERVED_COLORS]
        regular_tags = [tag for tag in tags if tag not in special_tags]

        for tag in sorted(special_tags):
            html += tag_html(tag)

        for tag in sorted(regular_tags):
            html += tag_html(tag)

        return html

    @env.macro
    def implementation(plugin, images):
        html = ""
        html += '<details style="margin-bottom: 15px;">'
        html += '<summary><span class="not-selectable" style="cursor: pointer;"><strong>Implementation</strong></span></summary>'
        html += f"<p><strong>Plugin:</strong> {plugin}."

        for image in images:
            html += f'<img style="margin-top: 15px;" src="{image}">'

        html += "</p></details>"

        return html


def on_pre_page_macros(env):
    env.conf[
        "copyright"
    ] = f"Documentation based on commit {env.variables['git']['short_commit']}."
