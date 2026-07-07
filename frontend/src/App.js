import { useState } from 'react';
import './App.css';

function AgeResultPanel({ data }) {
  if (!data) {
    return null;
  }

  const { years, months, days, total_days, fun_facts } = data;

  return (
    <section className="result-panel">
      <h2>Age Breakdown</h2>
      <div className="breakdown-grid">
        <div>
          <span className="label">Years</span>
          <strong>{years}</strong>
        </div>
        <div>
          <span className="label">Months</span>
          <strong>{months}</strong>
        </div>
        <div>
          <span className="label">Days</span>
          <strong>{days}</strong>
        </div>
        <div>
          <span className="label">Total days lived</span>
          <strong>{total_days.toLocaleString()}</strong>
        </div>
      </div>
      <div className="facts">
        <h3>Fun Facts</h3>
        <ul>
          {fun_facts.map((fact) => (
            <li key={fact}>{fact}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function App() {
  const [birthdate, setBirthdate] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!birthdate) {
      setError('Please select a birthdate first.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/age', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ birthdate }),
      });

      const contentType = response.headers.get('content-type') || '';
      const isJson = contentType.includes('application/json');

      let data;
      if (isJson) {
        data = await response.json();
      } else {
        const text = await response.text();
        throw new Error(
          `Server returned unexpected content: ${text.trim().slice(0, 300)}${text.length > 300 ? '…' : ''}`
        );
      }

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to calculate your age right now.');
      }

      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header>
        <div>
          <p className="eyebrow">Age Fun Facts</p>
          <h1>How long have you been on Earth?</h1>
          <p className="subtitle">
            Enter your birthdate to see your years, months, and days lived along with fun tidbits based on your age.
          </p>
        </div>
      </header>

      <main>
        <form className="calculator" onSubmit={handleSubmit}>
          <label htmlFor="birthdate">Your birthdate</label>
          <input
            id="birthdate"
            type="date"
            value={birthdate}
            onChange={(event) => setBirthdate(event.target.value)}
            max={new Date().toISOString().split('T')[0]}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Calculating...' : 'Calculate Age'}
          </button>
          {error && <p className="error">{error}</p>}
        </form>
        <AgeResultPanel data={result} />
      </main>
    </div>
  );
}

export default App;
