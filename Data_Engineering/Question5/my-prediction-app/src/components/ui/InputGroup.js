'use client';

export default function InputGroup({ label, name, type = "text", value, onChange, placeholder, error }) {
  return (
    <div style={{ marginBottom: '15px' }}>
      <label style={{ display: 'block', fontSize: '0.9rem', fontWeight: 'bold', color: '#374151', marginBottom: '5px' }}>
        {label} <span style={{ color: 'red' }}>*</span>
      </label>
      
      <input
        name={name}
        type="text"
        inputMode="numeric"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        style={{
          width: '100%',
          padding: '10px 12px',
          borderRadius: '6px',
          border: error ? '1px solid #ef4444' : '1px solid #d1d5db',
          backgroundColor: error ? '#fef2f2' : 'white',
          fontSize: '1rem',
          outline: 'none',
          color: '#000000',
          boxSizing: 'border-box'
        }}
      />
      
      {error && (
        <span style={{ color: '#ef4444', fontSize: '0.75rem', marginTop: '4px', display: 'block' }}>
          ⚠️ {error}
        </span>
      )}
    </div>
  );
}