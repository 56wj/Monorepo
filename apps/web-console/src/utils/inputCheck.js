export function check(number) {
    number = number
                 .replace(/[^\-\d.]/g, '')  //只能输入   数字 小数点 -
                 .replace(/\-{2,}/g, "-") // 只能出现一次- 
                 .replace(/^0+(\d)/, '$1') //如果第一位是 0 就替换成后面的数字
                 .replace(/^\./, '0.') //如果第一位是 . 就 替换成  0.
                 .match(/^[\d\-]*(\.?\d{0,5})/g)[0] || ''  //开头只能允许数字或者 -
    return number
  }

export function save(number) {
    number = parseFloat(number)
    return number
  }

  export function palletDataCheck(data) {
    // const keys = ['diameter', 'name', 'number', 'order_height', 'order_thickness', 'priority', 'real_height', 'real_thickness', 'weight', 'width']
    // const keyc = ['直径', '品名', '订单卷数', '订单长度', '订单厚度', '优先级', '实际生产米数', '实际厚度', '订单重量', '宽度']
    // const keys = ['name', 'order_thickness', 'real_thickness', 'width', 'order_height', 'real_height', 'number', 'weight', 'priority']
    // const keyc = ['品名', '订单厚度', '实际厚度', '宽度', '订单长度', '实际生产米数', '订单卷数', '订单重量', '优先级']
    // const keys = ['name', 'real_thickness', 'width', 'real_height', 'number', 'density']
    // const keyc = ['品名', '厚度', '宽度', '长度', '卷数', '密度']
    const keys = ['name', 'order_thickness', 'real_thickness', 'width', 'order_height', 'real_height', 'number', 'density']
    const keyc = ['品名', '订单厚度', '厚度', '宽度', '订单长度', '长度', '卷数', '密度']
    // const regex = /^\d+(\.\d+)?$/
    if(data.length==0||data==null){
      alert("订单数据为空，请检查！");
      return false;
    }
    for(let i = 0; i < data.length; i++) {
      for(let j = 0; j < keys.length; j++) {
        if(data[i][keys[j]] === undefined || String(data[i][keys[j]]).trim() === '') {
          // 空字符检查
          const str = `第${i+1}条数据的${keyc[j]}字段为空，请检查！`;
          alert(str);
          return false;
        }else if(j!=0){
          // 数字检查 判断是否为数字类型
          if(!isIntegerOrFloat(data[i][keys[j]])){
            const str = `第${i+1}条数据的${keyc[j]}字段不是数字，请检查！`;
            alert(str);
            return false;
          }
          // if(!regex.test(String(data[i][keys[j]]))) {
          //   const str = `第${i+1}条数据的${keyc[j]}字段不是数字，请检查！`;
          //   alert(str);
          //   return false;
          // }
        }
      }
    }
    return true;
  }

function isIntegerOrFloat(value) {
    return typeof value === 'number' && !isNaN(value);
}
