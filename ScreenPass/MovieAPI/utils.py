html_content = """
<html>
    <head>
        <title>ScreenPass API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                text-align: center;
                padding-top: 80px;
            }
            .container {
                background: #fff;
                padding: 40px 30px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                display: inline-block;
            }
            h1 {
                color: #2c3e50;
            }
            p {
                color: #555;
                margin-bottom: 30px;
            }
            .swagger-btn {
                background: #007bff;
                color: #fff;
                border: none;
                padding: 12px 28px;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                text-decoration: none;
                transition: background 0.2s;
            }
            .swagger-btn:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to ScreenPass API</h1>
            <p>Your one-stop solution for movie ticket booking!</p>
            <a href="/swagger" class="swagger-btn">View Swagger Documentation</a>
        </div>
    </body>
</html>
"""