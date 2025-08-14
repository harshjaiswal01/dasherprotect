import React, { useState } from 'react';
import { pingHello } from '../api';

export default function IdentifyPanel() {
  const [msg, setMsg] = useState<string>("(not called)");
  const [loading, setLoading] = useState(false);

  const onTest = async () => {
    setLoading(true);
    setMsg("(loading…)");
    try {
      const data = await pingHello();
      setMsg(JSON.stringify(data, null, 2));
    } catch (err: any) {
      setMsg(`ERROR: ${err?.message || String(err)}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-4 p-3 border rounded">
      <button
        className="px-3 py-2 border rounded"
        onClick={onTest}
        disabled={loading}
      >
        {loading ? 'Calling…' : 'Test API'}
      </button>
      <pre className="mt-3 text-sm whitespace-pre-wrap">{msg}</pre>
    </div>
  );
}
