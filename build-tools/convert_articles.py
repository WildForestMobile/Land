#!/usr/bin/env python3
"""
Convert REWRITTEN markdown articles to HTML format
"""
import re
import os
from pathlib import Path

def markdown_to_html(md_content, article_num):
    """Convert markdown content to HTML"""
    html_content = md_content
    
    # Remove markdown code blocks markers
    html_content = re.sub(r'```+\w*\n?', '', html_content)
    
    # Convert headers (starting from ##, as # is main title)
    html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    
    # Convert bold text **text** to <strong>
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # Convert italic *text* to <em>
    html_content = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', html_content)
    
    # Convert inline code `code` to <code>
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    
    # Convert links [text](url) to <a> and fix .md to .html
    def convert_link(match):
        text = match.group(1)
        url = match.group(2)
        # Replace .md with .html for article links
        if url.endswith('.md') or '-REWRITTEN.md' in url:
            url = re.sub(r'article-(\d+)(-REWRITTEN)?\.md', r'article-\1.html', url)
        return f'<a href="{url}">{text}</a>'
    
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', convert_link, html_content)
    
    # Convert unordered lists
    lines = html_content.split('\n')
    in_ul = False
    result_lines = []
    
    for i, line in enumerate(lines):
        # Handle unordered lists
        if re.match(r'^[\-\*] ', line):
            if not in_ul:
                result_lines.append('<ul>')
                in_ul = True
            item = re.sub(r'^[\-\*] ', '', line)
            result_lines.append(f'<li>{item}</li>')
        else:
            if in_ul:
                result_lines.append('</ul>')
                in_ul = False
            result_lines.append(line)
    
    if in_ul:
        result_lines.append('</ul>')
    
    html_content = '\n'.join(result_lines)
    
    # Convert paragraphs (lines that aren't already HTML and aren't empty)
    lines = html_content.split('\n')
    result_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<') and line != '---' and not line.startswith('**Article'):
            result_lines.append(f'<p>{line}</p>')
        elif line == '---':
            result_lines.append('<hr>')
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def extract_title(md_content):
    """Extract the main title from markdown (first # header)"""
    match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    return match.group(1) if match else "Article Title"

def extract_description(md_content):
    """Extract a description from the content"""
    # Remove the title
    content = re.sub(r'^# .+$', '', md_content, flags=re.MULTILINE)
    # Find first paragraph
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith('#') and not p.strip().startswith('**Article')]
    if paragraphs:
        desc = paragraphs[0][:200]
        # Clean markdown
        desc = re.sub(r'\*\*(.+?)\*\*', r'\1', desc)
        desc = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', desc)
        return desc
    return "Game development insights from Wild Forest Studio"

def create_html_article(md_content, article_num):
    """Create complete HTML article from markdown"""
    title = extract_title(md_content)
    description = extract_description(md_content)
    body_html = markdown_to_html(md_content, article_num)
    
    # Determine navigation
    prev_link = f"<a href='article-{article_num-1}.html' class='nav-prev'><i class='fas fa-chevron-left'></i> Previous Article</a>" if article_num > 1 else ""
    next_link = f"<a href='article-{article_num+1}.html' class='nav-next'>Next Article <i class='fas fa-chevron-right'></i></a>" if article_num < 7 else ""
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="keywords" content="game development, game design, indie games, virality, game mechanics">
    <meta name="author" content="Wild Forest Studio">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">

    <title>{title} | Wild Forest Studio</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@700;800&family=Roboto+Mono:wght@500;700&display=swap" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            /* Primary Colors */
            --primary-bg: #FFFFFF;
            --secondary-bg: #F8F9FA;
            --accent-bg: #F0F4FF;

            /* Text Colors */
            --text-primary: #1a1a2e;
            --text-secondary: #4a5568;
            --text-muted: #718096;

            /* Accent Colors */
            --accent-primary: #0066FF;
            --accent-secondary: #00D9FF;
            --accent-success: #00C48C;
            --accent-warning: #FF6B6B;

            /* Borders & Shadows */
            --border-color: #E2E8F0;
            --shadow-light: 0 2px 8px rgba(0, 0, 0, 0.08);
            --shadow-medium: 0 4px 16px rgba(0, 0, 0, 0.12);
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background: var(--primary-bg);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            line-height: 1.2;
        }}

        .metric-number {{
            font-family: 'Roboto Mono', monospace;
        }}

        /* Navigation */
        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            z-index: 1000;
            padding: 1rem 2rem;
            border-bottom: 1px solid var(--border-color);
            box-shadow: var(--shadow-light);
        }}

        nav .container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--text-primary);
            text-decoration: none;
        }}

        .nav-links {{
            display: flex;
            gap: 2rem;
            list-style: none;
        }}

        .nav-links a {{
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
            position: relative;
        }}

        .nav-links a:hover {{
            color: var(--accent-primary);
        }}

        .nav-links a:hover::after {{
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--accent-primary);
        }}

        .nav-cta {{
            background: var(--accent-primary);
            color: white;
            padding: 0.6rem 1.5rem;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .nav-cta:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 102, 255, 0.3);
        }}

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        /* Article Section */
        .article-section {{
            background: var(--primary-bg);
            padding: 8rem 0 5rem 0;
        }}

        .article-header {{
            margin-bottom: 3rem;
            text-align: center;
        }}

        .article-header h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        .article-meta {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}

        .article-meta span {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .article-meta .read-time,
        .article-meta .article-date,
        .article-meta .article-author {{
            padding: 0.5rem 1rem;
            background: var(--secondary-bg);
            border-radius: 20px;
            border: 1px solid var(--border-color);
        }}

        .article-content {{
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.8;
        }}

        .article-content h1,
        .article-content h2,
        .article-content h3,
        .article-content h4 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        .article-content h1 {{
            font-size: 2rem;
        }}

        .article-content h2 {{
            font-size: 1.8rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        .article-content h3 {{
            font-size: 1.5rem;
            color: var(--accent-primary);
        }}

        .article-content h4 {{
            font-size: 1.2rem;
        }}

        .article-content p {{
            margin-bottom: 1.5rem;
            color: var(--text-secondary);
        }}

        .article-content ul,
        .article-content ol {{
            margin-bottom: 1.5rem;
            padding-left: 2rem;
        }}

        .article-content li {{
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
        }}

        .article-content strong {{
            font-weight: 700;
            color: var(--text-primary);
        }}

        .article-content em {{
            font-style: italic;
        }}

        .article-content code {{
            background: var(--secondary-bg);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Roboto Mono', monospace;
            font-size: 0.9em;
            color: var(--accent-primary);
        }}

        .article-content pre {{
            background: var(--secondary-bg);
            padding: 1.5rem;
            border-radius: 5px;
            overflow-x: auto;
            margin: 1.5rem 0;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-primary);
        }}

        .article-content pre code {{
            background: none;
            padding: 0;
        }}

        .article-content hr {{
            border: none;
            border-top: 2px solid var(--border-color);
            margin: 2rem 0;
        }}

        .article-content blockquote {{
            border-left: 4px solid var(--accent-primary);
            padding-left: 1rem;
            margin: 1.5rem 0;
            font-style: italic;
            color: var(--text-secondary);
            background: var(--accent-bg);
            padding: 1rem;
            border-radius: 5px;
        }}

        .article-footer {{
            max-width: 800px;
            margin: 3rem auto 0;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
        }}

        .article-actions {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}

        .btn {{
            padding: 0.8rem 1.5rem;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .btn-secondary {{
            background: var(--accent-primary);
            color: white;
        }}

        .btn-secondary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 102, 255, 0.3);
        }}

        .btn-outline {{
            background: transparent;
            color: var(--accent-primary);
            border: 2px solid var(--accent-primary);
        }}

        .btn-outline:hover {{
            background: var(--accent-primary);
            color: white;
        }}

        .article-navigation {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .nav-prev,
        .nav-next {{
            color: var(--accent-primary);
            text-decoration: none;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s;
        }}

        .nav-prev:hover,
        .nav-next:hover {{
            gap: 0.8rem;
        }}

        /* Footer */
        footer {{
            background: var(--text-primary);
            padding: 3rem 2rem 1.5rem;
            border-top: 1px solid var(--border-color);
            color: white;
        }}

        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 3rem;
        }}

        .footer-section h4 {{
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: var(--accent-primary);
        }}

        .footer-section p,
        .footer-section a {{
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            display: block;
            margin-bottom: 0.5rem;
        }}

        .footer-section a:hover {{
            color: var(--accent-primary);
        }}

        .social-links {{
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }}

        .social-links a {{
            font-size: 1.5rem;
            color: white;
            transition: color 0.3s;
        }}

        .social-links a:hover {{
            color: var(--accent-primary);
        }}

        .newsletter-form {{
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
        }}

        .newsletter-form input {{
            flex: 1;
            padding: 0.8rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            color: white;
        }}

        .newsletter-form button {{
            padding: 0.8rem 1.5rem;
            background: var(--accent-primary);
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
        }}

        .footer-bottom {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.6);
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .article-header h1 {{
                font-size: 2rem;
            }}

            .nav-links {{
                display: none;
            }}

            .article-navigation {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="container">
            <a href="../index.html" class="logo">Wild Forest Studio</a>
            <ul class="nav-links">
                <li><a href="../index.html#problem">Problem</a></li>
                <li><a href="../index.html#solution">Solution</a></li>
                <li><a href="../index.html#proof">Track Record</a></li>
                <li><a href="../index.html#insights">Insights</a></li>
                <li><a href="../index.html#pricing">Pricing</a></li>
            </ul>
            <a href="../index.html#contact" class="nav-cta">Get Free Audit</a>
        </div>
    </nav>

    <!-- Article Content -->
    <section class="article-section">
        <div class="container">
            <div class="article-header">
                <h1>{title}</h1>
                <div class="article-meta">
                    <span class="read-time">10 min read</span>
                    <span class="article-date">November 2024</span>
                    <span class="article-author">Wild Forest Studio</span>
                </div>
            </div>
            <div class="article-content">
                {body_html}
            </div>
            <div class="article-footer">
                <div class="article-actions">
                    <a href="../index.html#insights" class="btn btn-outline">
                        <i class="fas fa-arrow-left"></i> Back to Articles
                    </a>
                </div>
                <div class="article-navigation">
                    {prev_link}
                    {next_link}
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h4>Wild Forest Studio</h4>
                <p>Crisis-proof game development partner delivering results since 2018.</p>
                <div class="social-links">
                    <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a>
                    <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                    <a href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
                    <a href="#" aria-label="Steam"><i class="fab fa-steam"></i></a>
                </div>
            </div>
            <div class="footer-section">
                <h4>Contact</h4>
                <p>Email: business@wildforeststudio.com</p>
                <p>Partnerships: partnerships@wildforeststudio.com</p>
                <p>Response time: Within 24 hours</p>
                <p>Hours: Mon-Fri, 9AM-6PM UTC+3</p>
            </div>
            <div class="footer-section">
                <h4>Services</h4>
                <a href="../index.html#services">Full-Cycle Development</a>
                <a href="../index.html#services">Viral Concept Design</a>
                <a href="../index.html#services">Publisher Negotiations</a>
                <a href="../index.html#services">LiveOps Support</a>
            </div>
            <div class="footer-section">
                <h4>Monthly Insights</h4>
                <p>Get expert insights on game dev survival</p>
                <form class="newsletter-form">
                    <input type="email" placeholder="Your email" required>
                    <button type="submit">Subscribe</button>
                </form>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 Wild Forest Studio. All rights reserved. | 272K+ wishlists generated | Successfully funded projects | 100% completion rate</p>
        </div>
    </footer>

    <script>
        // Scroll animations
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver(function(entries) {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, observerOptions);

        document.querySelectorAll('section').forEach(section => {{
            observer.observe(section);
        }});

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});

        // Newsletter form
        document.querySelector('.newsletter-form').addEventListener('submit', function(e) {{
            e.preventDefault();
            const email = this.querySelector('input').value;
            console.log('Newsletter subscription:', email);
            alert('Thank you for subscribing!');
            this.reset();
        }});
    </script>
</body>
</html>
"""
    
    return html_template

def main():
    """Main conversion function"""
    articles_dir = Path("f:/Projects/101/Land/articles")
    
    # Process articles 1-7
    for i in range(1, 8):
        md_file = articles_dir / f"article-{i}-REWRITTEN.md"
        html_file = articles_dir / f"article-{i}.html"
        
        if md_file.exists():
            print(f"Converting article-{i}...")
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            html_content = create_html_article(md_content, i)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✓ Created {html_file.name}")
        else:
            print(f"⚠ Warning: {md_file.name} not found")
    
    print("\nConversion complete!")

if __name__ == "__main__":
    main()
