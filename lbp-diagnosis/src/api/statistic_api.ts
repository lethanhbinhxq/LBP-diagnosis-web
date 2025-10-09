import api from './axios_instance'

export const getStatistics = async () => {
  const res = await api.get('/statistics/')
  return res.data
}