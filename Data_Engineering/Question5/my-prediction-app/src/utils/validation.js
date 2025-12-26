export const validatePredictionForm = (formData) => {
  const errors = {};

  if (!formData.customer_id) errors.customer_id = "ระบุ Customer ID";
  
  if (!formData.age) errors.age = "ระบุอายุ";
  else if (Number(formData.age) <= 0) errors.age = "อายุต้อง > 0";

  if (!formData.income) errors.income = "ระบุรายได้";
  else if (Number(formData.income) < 0) errors.income = "รายได้ห้ามติดลบ";

  if (!formData.avg_monthly_spend) errors.avg_monthly_spend = "ระบุยอดใช้จ่าย";
  else if (Number(formData.avg_monthly_spend) < 0) errors.avg_monthly_spend = "ยอดห้ามติดลบ";

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};