export const predictCustomerSegment = async (formData) => {
  try {
    const payload = {
      customer_id: formData.customer_id,
      features: {
        age: parseInt(formData.age),
        income: parseFloat(formData.income),
        avg_monthly_spend: parseFloat(formData.avg_monthly_spend)
      }
    };
    const response = await fetch(`http://localhost:8000/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to connect to Prediction API');
    }
    return await response.json();

  } catch (error) {
    console.error("API Error:", error);
    throw error; 
  }
};