import axios from 'axios';

// 백엔드 API의 기본 URL을 localhost:8000으로 설정합니다.
const API_URL = '/api/auth'; 

/**
 * 사용자 로그인을 위한 API 호출 함수입니다.
 * 이메일과 비밀번호를 백엔드에 전송합니다.
 * @param {string} email - 사용자 이메일
 * @param {string} password - 사용자 비밀번호
 * @returns {Promise<Object>} 서버로부터 받은 데이터 (성공 메시지, 토큰 등)
 */
export const login = async (email, password) => {
    try {
        const response = await axios.post(`${API_URL}/login`, {
            email,
            password,
        });
        return response.data;
    } catch (error) {
        console.error('Login Error:', error);
        throw error;
    }
};

/**
 * 사용자 회원가입을 위한 API 호출 함수입니다.
 * 이메일과 비밀번호를 백엔드에 전송합니다.
 * @param {string} email - 사용자 이메일
 * @param {string} password - 사용자 비밀번호
 * @returns {Promise<Object>} 서버로부터 받은 데이터 (성공 메시지 등)
 */
export const register = async (email, password) => {
    try {
        const response = await axios.post(`${API_URL}/register`, {
            email,
            password,
        });
        return response.data;
    } catch (error) {
        console.error('Register Error:', error);
        throw error;
    }
};

// ... 추가적인 인증 관련 함수를 여기에 구현할 수 있습니다.
// 예: 비밀번호 재설정, 사용자 정보 조회 등