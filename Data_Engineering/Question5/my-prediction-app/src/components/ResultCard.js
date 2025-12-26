'use client';

export default function ResultCard({ result }) {
  if (!result) return null;
  const getBadgeStyle = (prediction) => {
    const base = { padding: '8px 24px', borderRadius: '50px', fontWeight: 'bold', fontSize: '1.2rem', display: 'inline-block' };
    if (prediction === 'high') return { ...base, backgroundColor: '#ffffff', color: '#166534' };
    if (prediction === 'medium') return { ...base, backgroundColor: '#ffffff', color: '#854d0e' };
    return { ...base, backgroundColor: '#ffffff', color: '#ff0000ff' };
  };

  return (
    <div style={{ marginTop: '25px', padding: '20px', backgroundColor: '#ffffff', borderRadius: '12px', border: '1px solid #ffffff' }}>
      <h3 style={{ textAlign: 'center', color: '#000000ff', marginBottom: '15px' }}>Result</h3>
      
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <span style={getBadgeStyle(result.prediction)}>
          {result.prediction.toUpperCase()}
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        <div style={infoBox}>
          <small>Customer ID</small>
          <strong>{result.customer_id}</strong>
        </div>
        <div style={infoBox}>
          <small>Confidence</small>
          <strong>{(result.confidence * 100).toFixed(1)}%</strong>
        </div>
      </div>
    </div>
  );
}

const infoBox = { display: 'flex', flexDirection: 'column', alignItems: 'center', backgroundColor: '#64748b', padding: '10px', borderRadius: '8px', border: '1px solid #e2e8f0' };