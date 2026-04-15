import logfire

class ConfigureOTELService:
    def run(self):
        logfire.configure(send_to_logfire=False)  
        logfire.instrument_pydantic_ai()
        logfire.instrument_httpx(capture_all=True)