# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x | ✅ Active |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public GitHub issue.

Report vulnerabilities by emailing the maintainers directly or opening a private security advisory on GitHub:
Settings → Security → Advisories → New draft security advisory

We will respond within 72 hours and aim to patch within 14 days.

## Security Best Practices for Contributors

- **No hardcoded secrets**: All API keys and credentials must use `.env` / `st.secrets`
- **No absolute paths**: Use `pathlib.Path(__file__).parent` for all file paths
- **Input validation**: Sanitize all user inputs before use
- **HTML escaping**: Use `html.escape()` before rendering user-provided strings in `unsafe_allow_html`
- **No path traversal**: Never concatenate user input with file paths
- **Dependency pinning**: All dependencies must use exact `==` version pins in requirements.txt

## Environment Variables

Never commit `.env` files. Use `.env.example` as a template.
On Streamlit Cloud, use the Secrets management panel.
