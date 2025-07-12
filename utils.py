def respond_with_error(handler, code, message):
    default_messages = {
        404: "Not Found",
        500: "Internal Server Error",
        400: "Bad Request"
    }
    msg = message or default_messages.get(code, "Unknown Error")
    handler.log_message(f"Error {code}: {msg}")
    handler.send_response(code)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    handler.wfile.write(msg.encode())
    