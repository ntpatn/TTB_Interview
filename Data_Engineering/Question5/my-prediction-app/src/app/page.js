'use client';

import { useState } from 'react';
import InputGroup from '@/components/ui/InputGroup';
import ResultCard from '@/components/ResultCard';
import { validatePredictionForm } from '@/utils/validation';
import { predictCustomerSegment } from '@/services/apiService';

export default function Page() {
  const [formData, setFormData] = useState({ customer_id: '', age: '', income: '', avg_monthly_spend: '' });
  const [errors, setErrors] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const handleChange = (e) => {
    let { name, value } = e.target;
    value = value.replace(/\D/g, ''); 
    
    setFormData({ ...formData, [name]: value });
    if (errors[name]) setErrors({ ...errors, [name]: '' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');
    setResult(null);

    const validation = validatePredictionForm(formData);
    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    setLoading(true);
    try {
      const data = await predictCustomerSegment(formData);
      setResult(data);
    } catch (err) {
      setApiError(err.message || 'เชื่อมต่อ Server ไม่สำเร็จ');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#f1f5f9', padding: '20px' }}>
      <div style={{ backgroundColor: 'white', padding: '2.5rem', borderRadius: '16px', width: '100%', maxWidth: '500px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
        
        <h1 style={{ textAlign: 'center', color: '#2563eb', marginBottom: '10px' }}>Question 5</h1>
        <form onSubmit={handleSubmit}>
          <InputGroup label="Customer ID" type="text"name="customer_id" placeholder="กรุณาระบุ Customer ID" value={formData.customer_id} onChange={handleChange} error={errors.customer_id} />
          
          <div style={{ display: 'flex', gap: '15px' }}>
            <InputGroup label="Age" name="age" type="text" placeholder="กรุณาระบุอายุ" value={formData.age} onChange={handleChange} error={errors.age} />
            <InputGroup label="Income" name="income" type="text" placeholder="กรุณาระบุรายได้" value={formData.income} onChange={handleChange} error={errors.income} />
          </div>

          <InputGroup label="Monthly Spend" name="avg_monthly_spend" type="text" placeholder="กรุณาระบุค่าใช้จ่ายเฉลี่ยต่อเดือน" value={formData.avg_monthly_spend} onChange={handleChange} error={errors.avg_monthly_spend} />

          {apiError && <div style={{ padding: '10px', backgroundColor: '#fee2e2', color: '#991b1b', borderRadius: '6px', textAlign: 'center', marginBottom: '15px' }}>❌ {apiError}</div>}

          <button type="submit" disabled={loading} style={{ width: '100%', padding: '14px', backgroundColor: loading ? '#9ca3af' : '#2563eb', color: 'white', border: 'none', borderRadius: '8px', cursor: loading ? 'not-allowed' : 'pointer', fontWeight: 'bold' }}>
            {loading ? 'Processing...' : 'Commit'}
          </button>
        </form>

        <ResultCard result={result} />
        
      </div>
    </div>
  );
}