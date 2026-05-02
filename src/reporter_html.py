import sqlite3
import mjml
import pandas as pd
import os
from datetime import datetime

def generate_html_report():
    conn = sqlite3.connect('data/database.db')
    
    query = """
    SELECT title, price_float, scraped_at
    FROM books
    ORDER BY price_float DESC
    LIMIT 5
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    mjml_template = f"""
    <mjml>
      <mj-body background-color="#f4f4f4">
        <mj-section background-color="#ffffff" padding-bottom="0px">
          <mj-column width="100%">
            <mj-text font-size="20px" color="#333" font-family="helvetica">
              Daily Scraper Report: {datetime.now().strftime('%Y-%m-%d')}
            </mj-text>
            <mj-divider border-color="#f45e43"></mj-divider>
          </mj-column>
        </mj-section>
        <mj-section background-color="#ffffff">
          <mj-column>
            <mj-table>
                <tr style="border-bottom:1px solid #ecedee;text-align:left;padding:15px 0;">
                    <th style="padding: 0 15px 0 0; width: 80%;">Book Title</th>
                    <th style="padding: 0 15px; width: 20%;">Price</th>
                </tr>
                {"".join([f'<tr><td style="padding: 10px 15px 10px 0;">{row["title"]}</td><td style="padding: 10px 15px; white-space: nowrap;">£{row["price_float"]:.2f}</td></tr>' for _, row in df.iterrows()])}
            </mj-table>
          </mj-column>
        </mj-section>
      </mj-body>
    </mjml>
    """
    html_output = mjml.mjml_to_html(mjml_template)

    report_path = f"data/report/{datetime.now().strftime('%Y-%m-%d')}.html"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(html_output['html'])

    print(f"HTML report generated at: {report_path}")

if __name__ == "__main__":
    generate_html_report()