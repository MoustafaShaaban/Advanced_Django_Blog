import { useQuery } from '@tanstack/vue-query'
import { getAllTags } from '~/api/axios'

export function useItems() {

  const { data, error, isLoading, isError } = useQuery(['tags'], getAllTags)

  return {
    data,
    error,
    isLoading,
    isError
  }
}