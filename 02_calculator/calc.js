// let user = '2-3* (4-1) +5';
// let user = '(2+3)*((4-1)+5)';
// let user = '3+5*(4-6)/2';

const btnUser = document.getElementById('user');
const btnCalc = document.getElementById('calc');
const showResult = document.getElementById('result');

btnCalc.addEventListener('click', calc);  

function calc()
{
    let user = btnUser.value;
    // 1. 후위표현식으로 바꾸기
    let stack = [];
    let exp = [];
    const op = new Map([  //파이썬의 dict형과 유사
        ["(", 0], 
        ["+", 1],
        ["-", 1],
        ["*", 2],
        ["/", 2],
    ]);
    
    // user = user.replace(/\s/g, "")  // 모든(g) 공백(\s) 삭제(스페이스, 탭, 줄바꿈 등)
    user = user.replace(/[^0-9\+\-\*\/\(\)]/g, "");  // 숫자, 사칙연산기호, 괄호 이외의 모든 문자 삭제

    // 사용자가 입력한 수식의 괄호가 잘못되었는지 검사 코드 추가
    // user_arr = user.match(/[0-9\+\-\*\/\(\)]/g) || []; // 두 자릿수 숫자가 각각 저장되는 문제

    console.log( '사용자 입력 수식 -> ', user );
    for (let i=0; i<=user.length; i++)
    {
        if (!isNaN(user[i]))  // 숫자이면 후위식변수에 넣음
        {
            exp.push(parseInt(user[i]))
        } else if (stack.length==0 || user[i]=='(' || op.get(stack.slice(-1)[0])<op.get(user[i]) ) // 스택이 비었거나 수식문자가 여는괄호이거나 스택최상단연산자보다 우선순위가 크면
        {
            stack.push(user[i])
        } else if ( user[i]==')') // 수식문자가 닫는괄호이면
        {
            let tmp = '';
            while (stack.length != 0)
            {
                tmp = stack.pop();
                if (tmp=='(')
                {
                    break;
                } else
                {
                    exp.push(tmp);
                }
            }
        } else if ( op.get(stack.slice(-1)[0])>=op.get(user[i]) )  // 스택 최상단 연산자 우선순위보다 높지 않으면
        {
            while(op.get(stack.slice(-1)[0])>=op.get(user[i]) )  // 낮은 연산자를 만나기 전까지
            {
                exp.push(stack.pop());   // 스택의 기호를 차례로 pop -> exp.push
            }
            stack.push(user[i]);        // 인덱스의 기호 스택에 추가
        } else if ( i >= user.length)   // 수식문자를 모두 읽으면 남은 스택 모두 pop
        {
            while(stack.length != 0)
            {
                exp.push(stack.pop());
            }
        }
        //console.log('idx=', i, '수식=', user[i], ', stack -> ', stack, ', exp -> ', exp)
    }
    console.log('후위표현식 -> ', exp);

    // 2. 후위표현식 계산

    function exp_cal(oper, right, left)     // 먼저 pop한 것이 right
    {
        switch (oper) {
            case '+': stack.push(left + right); break;
            case '-': stack.push(left - right); break;
            case '*': stack.push(left * right); break;
            case '/': stack.push(left / right); break;
        }
    }

    for(let i=0; i<exp.length; i++)
    {
        if(!isNaN(exp[i]))
        {
            stack.push(exp[i]);
        } else if( exp[i] == '+')
        {
            exp_cal('+', stack.pop(), stack.pop());
        } else if( exp[i] == '-')
        {
            exp_cal('-', stack.pop(), stack.pop());
        } else if( exp[i] == '*')
        {
            exp_cal('*', stack.pop(), stack.pop());
        } else if( exp[i] == '/')
        {
            exp_cal('/', stack.pop(), stack.pop());
        }
        //console.log(i, '->', exp[i], '->', stack);
    }

    let result = stack.pop()
    // console.log('수식 계산값 = ', stack.pop());

showResult.innerText = result;
}