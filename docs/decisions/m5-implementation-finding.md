# Module 5 Implementation Finding

**Project:** DataMan  
**Module:** CTS-285 Module 5  
**Student:** Nicholas Candanoza

## Implementation Question

Can the product behavior already designed and tested survive the move into Flask without losing traceability, reusable logic, or a clear state/data boundary?

## Finding

The Flask implementation confirmed that the two-attempt answer flow can work with Flask while keeping the business rules separate from the interface.

The Flask routes handle requests and responses. The reusable logic in `dataman/logic.py` enforces the two-attempt rule. The `JsonFileStore` class in `dataman/store.py` saves and retrieves student progress.

## Evidence

1. Four Flask tests passed using `python -m pytest -v`.
2. The first incorrect answer allows one more attempt.
3. The second incorrect answer reveals the correct answer.
4. A correct answer completes the question.
5. Progress remains available across separate requests.
6. A manual restart test confirmed that progress remained at 1/2 attempts after Flask was stopped and restarted.

## What Flask Exposed

The restart test demonstrated that preserving progress requires both persistent JSON storage and a consistent player identity through the browser session.

The application also showed that Flask route code can coordinate the behavior without containing the two-attempt product rule itself.

## Decision

Keep the business rules in reusable Python logic, keep JSON storage behind the store boundary, and use Flask only for the web interface and request handling.

## Next Action

Add an automated test for persistence across application instances and improve the development secret-key configuration before extending the application.

## Traceability Note

The acceptance criterion in `docs/requirements.md` was reconstructed from available Module 4 evidence because the original Module 4 files were no longer available. The Flask tests and manual browser checks provide implementation evidence for the reconstructed criterion.